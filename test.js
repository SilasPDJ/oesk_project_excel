let findSpecificELement = (element, text) => {
    for (let el of document.querySelectorAll(element)) {
        if (el.textContent.includes(text)) {
            return el;
        }
    }
};

findSpecificELement("a", "Dívida Ativa").click()
