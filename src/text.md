Screens:
  Chat Screen:
    Children:
      - conMainScreen:
          Control: GroupContainer@1.3.0
          Variant: AutoLayout
          Properties:
            Fill: =RGBA(245, 245, 245, 1)
            Height: =Parent.Height
            LayoutAlignItems: =LayoutAlignItems.Stretch
            LayoutDirection: =LayoutDirection.Vertical
            Width: =Parent.Width
          Children:
            - conChatLayout:
                Control: GroupContainer@1.3.0
                Variant: AutoLayout
                Properties:
                  Fill: =Color.White
                  LayoutAlignItems: =LayoutAlignItems.Stretch
                  LayoutDirection: =LayoutDirection.Horizontal
                  LayoutWrap: =true
                Children:
                  - conChatListSidebar:
                      Control: GroupContainer@1.3.0
                      Variant: AutoLayout
                      Properties:
                        Fill: =RGBA(255, 255, 255, 1)
                        FillPortions: =3
                        LayoutDirection: =LayoutDirection.Vertical
                      Children:
                        - conUserProfileHeader:
                            Control: GroupContainer@1.3.0
                            Variant: AutoLayout
                            Properties:
                              Fill: =Color.WhiteSmoke
                              FillPortions: =0
                              Height: =75
                              LayoutAlignItems: =LayoutAlignItems.Center
                              LayoutDirection: =LayoutDirection.Horizontal
                              LayoutGap: =12
                              PaddingBottom: =12
                              PaddingLeft: =12
                              PaddingRight: =12
                              PaddingTop: =12
                            Children:
                              - imgUserProfile:
                                  Control: Image@2.2.3
                                  Properties:
                                    Height: =Parent.Height * 0.8
                                    Image: =User().Image
                                    RadiusBottomLeft: =Self.Height
                                    RadiusBottomRight: =Self.Height
                                    RadiusTopLeft: =Self.Height
                                    RadiusTopRight: =Self.Height
                                    Width: =Self.Height
                              - lblUserName:
                                  Control: Label@2.5.1
                                  Properties:
                                    FillPortions: =1
                                    OnSelect: =
                                    Size: =16
                                    Text: =Office365ユーザー.MyProfileV2().displayName
                        - conNewChatHeader:
                            Control: GroupContainer@1.3.0
                            Variant: AutoLayout
                            Properties:
                              Fill: =RGBA(255, 255, 255, 1)
                              FillPortions: =0
                              Height: =75
                              LayoutAlignItems: =LayoutAlignItems.Center
                              LayoutDirection: =LayoutDirection.Horizontal
                              LayoutGap: =12
                              PaddingLeft: =12
                              PaddingRight: =12
                              RadiusBottomLeft: =0
                              RadiusBottomRight: =0
                              RadiusTopLeft: =0
                              RadiusTopRight: =0
                            Children:
                              - icoNewChat:
                                  Control: Classic/Icon@2.5.0
                                  Properties:
                                    Height: =32
                                    Icon: =Icon.Add
                                    OnSelect: |-
                                      =UpdateContext({locMessageID: ""});
                                      Clear(colChat);
                                      UpdateContext({locFilter: false});
                                      UpdateContext({locFilter: true});
                                    Width: =32
                              - lblicoNewChat:
                                  Control: Label@2.5.1
                                  Properties:
                                    AutoHeight: =true
                                    FillPortions: =1
                                    OnSelect: =Select(icoNewChat);
                                    Text: =$"新しいチャット"
                                    X: =76
                                    Y: =8
                        - galChatList:
                            Control: Gallery@2.15.0
                            Variant: Vertical
                            Properties:
                              Items: =Filter('sp-chatlib',locFilter)
                              OnSelect: |
                                =UpdateContext({locMessageID: ThisItem.MessageID});
                                ClearCollect(
                                    colChat,
                                    ForAll(
                                        Table(ParseJSON('get-json-content'.Run(locMessageID).response).Log) As Result,
                                        {
                                            MessageIndex: Value(Result.Value.MessageIndex),
                                            MessageText: Text(Result.Value.MessageText),
                                            SenderName: Text(Result.Value.SenderName),
                                            TimeStamp: DateTimeValue(Result.Value.TimeStamp)
                                        }
                                    )
                                );
                              TemplateFill: |-
                                =If(
                                    ThisItem.MessageID = locMessageID,
                                    App.Theme.Colors.Lighter80,
                                    RGBA(
                                        0,
                                        0,
                                        0,
                                        0
                                    )
                                )
                              TemplatePadding: =0
                              TemplateSize: =If(Self.Layout = Layout.Horizontal, Min(96, Self.Width - 60), Min(96, Self.Height - 60))
                            Children:
                              - lblChatTitle:
                                  Control: Label@2.5.1
                                  Properties:
                                    FontWeight: |-
                                      =If(
                                          ThisItem.MessageID = locMessageID,
                                          FontWeight.Semibold,
                                          FontWeight.Normal
                                      )
                                    OnSelect: =Select(Parent)
                                    Size: =12
                                    Text: =ThisItem.Subject
                                    Width: =240
                                    X: =76
                                    Y: =8
                              - txtAvatar:
                                  Control: Classic/TextInput@2.3.2
                                  Properties:
                                    Align: =Align.Center
                                    Default: =Left(ThisItem.Subject,1)
                                    DisabledColor: |-
                                      =If(
                                          ThisItem.MessageID = locMessageID,
                                          Color.White,
                                          Color.Black
                                      )
                                    DisabledFill: |-
                                      =If(
                                          ThisItem.MessageID = locMessageID,
                                          App.Theme.Colors.Darker40,
                                          Color.White
                                      )
                                    DisplayMode: =DisplayMode.Disabled
                                    Height: =52
                                    OnSelect: =Select(Parent)
                                    PaddingBottom: =0
                                    PaddingLeft: =0
                                    PaddingRight: =0
                                    PaddingTop: =0
                                    Width: =52
                                    X: =12
                                    Y: =20
                              - lblCreatedTime:
                                  Control: Label@2.5.1
                                  Properties:
                                    AutoHeight: =true
                                    Height: =24
                                    OnSelect: =Select(Parent)
                                    Text: =DateTimeValue(ThisItem.CreatedTime)
                                    Width: =325
                                    X: =76
                                    Y: =48
                  - conChatMain:
                      Control: GroupContainer@1.3.0
                      Variant: AutoLayout
                      Properties:
                        Fill: =Color.WhiteSmoke
                        FillPortions: =7
                        LayoutDirection: =LayoutDirection.Vertical
                      Children:
                        - conChatHeader:
                            Control: GroupContainer@1.3.0
                            Variant: AutoLayout
                            Properties:
                              Fill: =ColorFade(ColorValue("#F5F5F5"),50%)
                              FillPortions: =0
                              Height: =Parent.Height * 0.12
                              LayoutAlignItems: =LayoutAlignItems.Center
                              LayoutDirection: =LayoutDirection.Horizontal
                              LayoutGap: =8
                              PaddingLeft: =12
                              PaddingRight: =12
                              RadiusBottomLeft: =0
                              RadiusBottomRight: =0
                              RadiusTopLeft: =0
                              RadiusTopRight: =0
                            Children:
                              - icoChatHeader:
                                  Control: Image@2.2.3
                                  Properties:
                                    Height: =Parent.Height * 0.9
                                    Image: "=\"data:image/svg+xml;utf8, \" & EncodeUrl(\"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'>\r\n  \r\n  <circle cx='12' cy='12' r='11' fill='#128C7E'/>\r\n  \r\n  <path\r\n    d='M6 8.5C6 7.67157 6.67157 7 7.5 7H16.5C17.3284 7 18 7.67157 18 8.5V13.5C18 14.3284 17.3284 15 16.5 15H13L12 17L11 15H7.5C6.67157 15 6 14.3284 6 13.5V8.5Z'\r\n    fill='white'\r\n  />\r\n  <circle cx='9' cy='11' r='0.8' fill='#128C7E'/>\r\n  <circle cx='12' cy='11' r='0.8' fill='#128C7E'/>\r\n  <circle cx='15' cy='11' r='0.8' fill='#128C7E'/>\r\n</svg>\")"
                                    OnSelect: =Clear(colChat);
                                    Width: =Self.Height
                              - lblChatHeader:
                                  Control: Label@2.5.1
                                  Properties:
                                    AlignInContainer: =AlignInContainer.Center
                                    AutoHeight: =true
                                    FillPortions: =1
                                    Text: =LookUp('sp-chatlib',MessageID = locMessageID).Subject
                                    Visible: =!IsBlank(locMessageID)
                                    X: =76
                                    Y: =8
                        - galMessages:
                            Control: Gallery@2.15.0
                            Variant: VariableHeight
                            Properties:
                              Items: =colChat
                              TemplatePadding: =4
                              TemplateSize: '=72  '
                            Children:
                              - htmlMessageContent:
                                  Control: HtmlViewer@2.1.0
                                  Properties:
                                    AutoHeight: =true
                                    Font: =Font.'Open Sans'
                                    Height: =72
                                    HtmlText: |-
                                      =With(
                                          {
                                              avatarStyle: "width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 14px;",
                                              messageWrapperBase: "max-width: 70%; margin-bottom: 16px; display: flex; gap: 8px;",
                                              messageBubbleBase: "padding: 8px 12px; border-radius: 8px; box-shadow: 0 1px 2px rgba(0,0,0,0.1);",
                                              nameStyle: "font-size: 12px; color: #666666; margin-bottom: 4px;",
                                              timeStyle: "font-size: 11px; color: #666666; text-align: right;"
                                          },
                                          Switch(
                                              Mod(ThisItem.MessageIndex, 2),
                                              0,
                                              $"<div style='{messageWrapperBase} margin-right: auto;'>
                                                  <div style='{avatarStyle} background-color: #e0e0e0;'>
                                                      {Left(ThisItem.SenderName, 2)}
                                                  </div>
                                                  <div>
                                                      <div style='{nameStyle}'>{ThisItem.SenderName}</div>
                                                      <div style='{messageBubbleBase} background-color: #ffffff;'>
                                                          <div style='margin-bottom: 4px;'>{ThisItem.MessageText}</div>
                                                          <div style='{timeStyle}'>{ThisItem.TimeStamp}</div>
                                                      </div>
                                                  </div>
                                              </div>",
                                              1,
                                              $"<div style='{messageWrapperBase} margin-left: auto; flex-direction: row-reverse;'>
                                                  <div style='{avatarStyle} background-color: #128C7E; color: white;'>Me</div>
                                                  <div>
                                                      <div style='{nameStyle} text-align: right;'>自分</div>
                                                      <div style='{messageBubbleBase} background-color: #dcf8c6;'>
                                                          <div style='margin-bottom: 4px;'>{ThisItem.MessageText}</div>
                                                          <div style='{timeStyle}'>{ThisItem.TimeStamp}</div>
                                                      </div>
                                                  </div>
                                              </div>"
                                          )
                                      )
                                    OnSelect: =Select(Parent)
                                    Width: =Parent.TemplateWidth - 24
                                    X: =12
                        - conMessageInput:
                            Control: GroupContainer@1.3.0
                            Variant: AutoLayout
                            Properties:
                              Fill: =ColorFade(ColorValue("#F5F5F5"),50%)
                              FillPortions: =0
                              Height: =Parent.Height * 0.12
                              LayoutAlignItems: =LayoutAlignItems.Center
                              LayoutDirection: =LayoutDirection.Horizontal
                              LayoutGap: =12
                              PaddingLeft: =12
                              PaddingRight: =12
                              RadiusBottomLeft: =0
                              RadiusBottomRight: =0
                              RadiusTopLeft: =0
                              RadiusTopRight: =0
                            Children:
                              - inpMessageText:
                                  Control: Classic/TextInput@2.3.2
                                  Properties:
                                    BorderThickness: =1
                                    Default: =
                                    FillPortions: =1
                                    Height: =52
                                    RadiusBottomLeft: =8
                                    RadiusBottomRight: =8
                                    RadiusTopLeft: =8
                                    RadiusTopRight: =8
                              - btnSendMessage:
                                  Control: Button@0.0.45
                                  Properties:
                                    BorderRadius: =8
                                    Height: =52
                                    Icon: ="Chat"
                                    Layout: ='ButtonCanvas.Layout'.IconOnly
                                    OnSelect: "=If(\n    CountRows(colChat) = 0,\n    // Me\n    ClearCollect(\n        colChat,\n        {\n            MessageIndex: 1,\n            SenderName: Office365ユーザー.MyProfileV2().displayName,\n            MessageText: inpMessageText.Text,\n            TimeStamp: Now()\n        }\n    );\n    Collect(\n        colChat,\n        {\n            MessageIndex: (CountRows(colChat) + 1),\n            SenderName: \"AI Builder\",\n            MessageText: 'AI Reply'.Predict(inpMessageText.Text).Text,\n            TimeStamp: Now()\n        }\n    );\n    UpdateContext({locAiResponse: 'Custom-prompt-response'.Predict(inpMessageText.Text).StructuredOutput});\n    ,\n    Collect(\n        colChat,\n        {\n            MessageIndex: (CountRows(colChat) + 1),\n            SenderName: Office365ユーザー.MyProfileV2().displayName,\n            MessageText: inpMessageText.Text,\n            TimeStamp: Now()\n        }\n    );\n    Collect(\n        colChat,\n        {\n            MessageIndex: (CountRows(colChat) + 1),\n            SenderName: \"AI Builder\",\n            MessageText: 'AI Reply'.Predict(inpMessageText.Text).Text,\n            TimeStamp: Now()\n        }\n    );\n    \n);\nWith(\n    {\n        FirstPost: First(colChat),\n        LastPost: Last(colChat)\n    },\n    UpdateContext(\n        {\n            spMetaData: {\n                MessageID: Coalesce(\n                    locMessageID,\n                    Text(GUID())\n                ),\n                LastMessageText: LastPost.MessageText,\n                LastMessageTime: LastPost.TimeStamp,\n                LastSender: LastPost.SenderName,\n                MessageCount: CountRows(colChat),\n                CreateBy: FirstPost.SenderName,\n                CreatedTime: FirstPost.TimeStamp,\n                UpdatedTime: LastPost.TimeStamp,\n                Subject: Coalesce(\n                    locAiResponse.response,\n                    galChatList.Selected.Subject\n                ),\n                Fill: Coalesce(\n                    locAiResponse.fill,\n                    galChatList.Selected.Fill\n                ),\n                FontColor: Coalesce(\n                    locAiResponse.fontcolor,\n                    galChatList.Selected.FontColor\n                )\n            }\n        }\n    )\n);\nUpdateContext(\n    {\n        locMessageID: 'post-json-chat'.Run(\n            JSON(spMetaData),\n            JSON(\n                {Log: Table(colChat)},\n                JSONFormat.Compact\n            )\n        ).messageid\n    }\n);\nReset(inpMessageText);\nUpdateContext({locFilter: false});\nUpdateContext({locFilter: true});\n"
                                    Text: ="送信"
                                    Width: =52
