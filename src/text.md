let
    // 1. 開始日と終了日をパラメータとして設定
    StartDate = #date(2023, 1, 1), // 開始日を設定
    EndDate = #date(2024, 12, 31), // 終了日を設定

    // 日付のリストを生成
    DateList = List.Dates(StartDate, Duration.Days(EndDate - StartDate) + 1, #duration(1, 0, 0, 0)),

    // リストをテーブルに変換
    // 'Converted to Table' から 'ConvertedToTable' に変更
    ConvertedToTable = Table.FromList(DateList, Splitter.None, null, null, ExtraValues.Error),
    // 'Renamed Columns' から 'RenamedColumns' に変更
    RenamedColumns = Table.RenameColumns(ConvertedToTable,{{"Column1", "Date"}}),

    // 3. 各列のデータ型を明示的に設定し、必要な日付属性を追加
    // 'Changed Type' から 'ChangedType' に変更
    ChangedType = Table.TransformColumnTypes(RenamedColumns,{{"Date", type date}}),
    // 各日付属性の追加ステップ名も変更
    AddedYear = Table.AddColumn(ChangedType, "Year", each Date.Year([Date]), type number),
    AddedMonth = Table.AddColumn(AddedYear, "Month", each Date.Month([Date]), type number),
    AddedMonthName = Table.AddColumn(AddedMonth, "Month Name", each Date.MonthName([Date]), type text),
    AddedQuarter = Table.AddColumn(AddedMonthName, "Quarter", each Date.QuarterOfYear([Date]), type number),
    AddedDay = Table.AddColumn(AddedQuarter, "Day", each Date.Day([Date]), type number),
    AddedDayOfWeek = Table.AddColumn(AddedDay, "Day of Week", each Date.DayOfWeek([Date]), type number), // 0=日曜, 1=月曜...
    AddedDayName = Table.AddColumn(AddedDayOfWeek, "Day Name", each Date.DayOfWeekName([Date]), type text),
    AddedDayOfYear = Table.AddColumn(AddedDayName, "Day of Year", each Date.DayOfYear([Date]), type number),
    AddedWeekOfYear = Table.AddColumn(AddedDayOfYear, "Week of Year", each Date.WeekOfYear([Date]), type number),
    AddedWeekOfMonth = Table.AddColumn(AddedWeekOfYear, "Week of Month", each Date.WeekOfMonth([Date]), type number),
    AddedStartOfWeek = Table.AddColumn(AddedWeekOfMonth, "Start of Week", each Date.StartOfWeek([Date]), type date),
    AddedEndOfWeek = Table.AddColumn(AddedStartOfWeek, "End of Week", each Date.EndOfWeek([Date]), type date),
    AddedStartOfMonth = Table.AddColumn(AddedEndOfWeek, "Start of Month", each Date.StartOfMonth([Date]), type date),
    AddedEndOfMonth = Table.AddColumn(AddedStartOfMonth, "End of Month", each Date.EndOfMonth([Date]), type date),
    AddedStartOfQuarter = Table.AddColumn(AddedEndOfMonth, "Start of Quarter", each Date.StartOfQuarter([Date]), type date),
    AddedEndOfQuarter = Table.AddColumn(AddedStartOfQuarter, "End of Quarter", each Date.EndOfQuarter([Date]), type date),
    AddedStartOfYear = Table.AddColumn(AddedEndOfQuarter, "Start of Year", each Date.StartOfYear([Date]), type date),
    AddedEndOfYear = Table.AddColumn(AddedStartOfYear, "End of Year", each Date.EndOfYear([Date]), type date),
    AddedIsWeekend = Table.AddColumn(AddedEndOfYear, "Is Weekend", each if Date.DayOfWeek([Date]) = 0 or Date.DayOfWeek([Date]) = 6 then true else false, type logical),
    AddedFiscalYear = Table.AddColumn(AddedIsWeekend, "Fiscal Year", each if Date.Month([Date]) >= 4 then Date.Year([Date]) + 1 else Date.Year([Date]), type number), // 会計年度を4月始まりとする例

    // 必要に応じて列の順序を調整
    // 'Reordered Columns' から 'ReorderedColumns' に変更
    ReorderedColumns = Table.ReorderColumns(AddedFiscalYear,{"Date", "Year", "Month", "Month Name", "Quarter", "Day", "Day Name", "Day of Week", "Day of Year", "Week of Year", "Week of Month", "Start of Week", "End of Week", "Start of Month", "End of Month", "Start of Quarter", "End of Quarter", "Start of Year", "End of Year", "Is Weekend", "Fiscal Year"})
in
    ReorderedColumns
