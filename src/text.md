let
    // Step 1: Import the public holidays CSV file from the web with the appropriate delimiter and encoding
    ImportHolidaysCSV = Csv.Document(Web.Contents("https://www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv"), [Delimiter = ",", Columns = 2, Encoding = 932]),
    
    // Step 2: Promote the first row to headers
    PromoteHeaders = Table.PromoteHeaders(ImportHolidaysCSV, [PromoteAllScalars = true]),
    
    // Step 3: Change column types to match the correct data types (date and text)
    SetHolidayColumnTypes = Table.TransformColumnTypes(PromoteHeaders, {{"国民の祝日・休日月日", type date}, {"国民の祝日・休日名称", type text}}, "ja"),

    // Step 4: Get today's date
    CurrentDate = Date.From(DateTime.LocalNow()),

    // Step 5: Define the start date (January 1st of the previous year)
    PreviousYearStartDate = #date(Date.Year(CurrentDate) - 0, 1, 1),

    // Step 6: Define the end date (December 31st of the next year)
    NextYearEndDate = #date(Date.Year(CurrentDate) + 1, 12, 31),

    // Step 7: Generate a list of dates from PreviousYearStartDate to NextYearEndDate
    GenerateDateList = List.Dates(PreviousYearStartDate, Duration.Days(NextYearEndDate - PreviousYearStartDate) + 1, #duration(1, 0, 0, 0)),

    // Step 8: Convert the list of dates into a table
    CreateDateTable = Table.FromList(GenerateDateList, Splitter.SplitByNothing(), {"Date"}, null, ExtraValues.Error),

    // Step 9: Add an index column for sorting and identification
    AddIndexColumn = Table.AddIndexColumn(CreateDateTable, "Index", 1, 1, Int64.Type),

    // Step 10: Reorder the columns for clarity (index first, then date)
    ReorderColumns = Table.ReorderColumns(AddIndexColumn, {"Index", "Date"}),

    // Step 11: Merge the date table with the public holidays table on the date field
    MergeWithHolidays = Table.NestedJoin(ReorderColumns, {"Date"}, SetHolidayColumnTypes, {"国民の祝日・休日月日"}, "HolidayDetails", JoinKind.LeftOuter),

    // Step 12: Expand the holiday details to include the holiday name in the main table
    ExpandHolidayDetails = Table.ExpandTableColumn(MergeWithHolidays, "HolidayDetails", {"国民の祝日・休日名称"}, {"HolidayName"}),

    // Step 13: Add Year, Month, and Day columns from the Date column
    AddYearColumn = Table.AddColumn(ExpandHolidayDetails, "Year", each Date.Year([Date]), type number),
    AddMonthColumn = Table.AddColumn(AddYearColumn, "Month", each Date.Month([Date]), type number),
    AddDayColumn = Table.AddColumn(AddMonthColumn, "Day", each Date.Day([Date]), type number),

    // Step 14: Add TextYear and TextMonth columns for display purposes
    AddTextYearColumn = Table.AddColumn(AddDayColumn, "TextYear", each Text.From(Date.Year([Date])) & "年", type text),
    AddTextMonthColumn = Table.AddColumn(AddTextYearColumn, "TextMonth", each Text.From(Date.Month([Date])) & "月", type text),

    // Step 15: Localize the weekday column to Japanese (Monday to Sunday)
    AddLocalizedWeekdayColumn = Table.AddColumn(AddTextMonthColumn, "Weekday", each 
        if Date.DayOfWeek([Date], Day.Monday) = 0 then "月曜日" 
        else if Date.DayOfWeek([Date], Day.Monday) = 1 then "火曜日" 
        else if Date.DayOfWeek([Date], Day.Monday) = 2 then "水曜日"
        else if Date.DayOfWeek([Date], Day.Monday) = 3 then "木曜日"
        else if Date.DayOfWeek([Date], Day.Monday) = 4 then "金曜日"
        else if Date.DayOfWeek([Date], Day.Monday) = 5 then "土曜日"
        else "日曜日", type text),

    // Step 16: Add a column to flag holidays (Saturday, Sunday, or public holiday)
    AddHolidayFlagColumn = Table.AddColumn(AddLocalizedWeekdayColumn, "IsHoliday", each 
        if Date.DayOfWeek([Date], Day.Saturday) >= 5 or [HolidayName] <> null then true else false, type logical),

    // Step 17: Add Fiscal Year column based on Japanese fiscal year (April to March)
    AddFiscalYearColumn = Table.AddColumn(AddHolidayFlagColumn, "FiscalYear", each 
        if Date.Month([Date]) >= 4 then Date.Year([Date]) else Date.Year([Date]) - 1, type number),
  SetDataType = Table.TransformColumnTypes(AddFiscalYearColumn, {{"Date", type date}})
in
    SetDataType
