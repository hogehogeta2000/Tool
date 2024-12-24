$"<div style='{popupStyles.overlay}'>
    <div style='{popupStyles.container}'>
        <div style='{popupStyles.accentLine}'></div>
        <div style='{popupStyles.contentWrapper}'>
            <button style='{popupStyles.closeButton} aria-label='{popupTexts.close}'>
                <span style='{popupStyles.closeLine}; transform: rotate(45deg);'></span>
                <span style='{popupStyles.closeLine}; transform: rotate(-45deg);'></span>
            </button>
            <div style='{popupStyles.header}'>
                <h2 style='{popupStyles.title}'>
                    <span style='{popupStyles.infoIcon}'>{popupTexts.info}</span>
                    <span style='line-height: 1.2;'>{popupTexts.title}</span>
                </h2>
            </div>
            <div style='{popupStyles.content}'>
                <p style='margin: 0;'>{popupTexts.content}</p>
            </div>
            <div style='{popupStyles.buttonArea}'>
                <button style='{popupStyles.button}'>{popupTexts.button}</button>
            </div>
        </div>
    </div>
</div>"
