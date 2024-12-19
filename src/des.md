// まず、コレクションを作成する例
ClearCollect(
    colTableData,
    {
        Item: "A",
        Value: "100"
    },
    {
        Item: "B",
        Value: "200"
    },
    {
        Item: "C",
        Value: "300"
    }
);

// テーブルの生成
With(
    {
        // コンテナスタイル
        containerStyle: "max-width: fit-content; margin: 20px; background: white; border-radius: 12px; box-shadow: 0 4px 24px rgba(0, 0, 0, 0.06); padding: 8px;",
        
        // テーブルスタイル
        tableStyle: "border-collapse: separate; border-spacing: 0; width: auto; font-family: -apple-system, BlinkMacSystemFont, system-ui, sans-serif;",
        
        // ヘッダーセルの共通スタイル
        thStyle: "padding: 12px 20px; text-align: left; font-size: 14px; color: #6b7280; font-weight: 500; white-space: nowrap; border-bottom: 2px solid #f3f4f6;",
        
        // データセルの共通スタイル（境界線あり）
        tdStyleWithBorder: "padding: 12px 20px; text-align: left; font-size: 14px; color: #111827; border-bottom: 1px solid #f3f4f6;",
        
        // データセルの共通スタイル（境界線なし - 最終行用）
        tdStyleNoBorder: "padding: 12px 20px; text-align: left; font-size: 14px; color: #111827;"
    },
    
    // ヘッダー部分の生成
    "<div style='" & containerStyle & "'>" &
    "<table style='" & tableStyle & "'>" &
    "<tr>" &
        "<th style='" & thStyle & "'>項目</th>" &
        "<th style='" & thStyle & "'>値</th>" &
    "</tr>" &
    
    // コレクションからの動的な行生成
    Concat(
        colTableData,
        If(
            IsLast(),
            // 最終行の場合（境界線なし）
            "<tr>" &
                "<td style='" & tdStyleNoBorder & "'>" & Item & "</td>" &
                "<td style='" & tdStyleNoBorder & "'>" & Value & "</td>" &
            "</tr>",
            // それ以外の行（境界線あり）
            "<tr>" &
                "<td style='" & tdStyleWithBorder & "'>" & Item & "</td>" &
                "<td style='" & tdStyleWithBorder & "'>" & Value & "</td>" &
            "</tr>"
        )
    ) &
    
    "</table>" &
    "</div>"
)
