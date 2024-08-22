const linkSvg = `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 512"><path d="M579.8 267.7c56.5-56.5 56.5-148 0-204.5c-50-50-128.8-56.5-186.3-15.4l-1.6 1.1c-14.4 10.3-17.7 30.3-7.4 44.6s30.3 17.7 44.6 7.4l1.6-1.1c32.1-22.9 76-19.3 103.8 8.6c31.5 31.5 31.5 82.5 0 114L422.3 334.8c-31.5 31.5-82.5 31.5-114 0c-27.9-27.9-31.5-71.8-8.6-103.8l1.1-1.6c10.3-14.4 6.9-34.4-7.4-44.6s-34.4-6.9-44.6 7.4l-1.1 1.6C206.5 251.2 213 330 263 380c56.5 56.5 148 56.5 204.5 0L579.8 267.7zM60.2 244.3c-56.5 56.5-56.5 148 0 204.5c50 50 128.8 56.5 186.3 15.4l1.6-1.1c14.4-10.3 17.7-30.3 7.4-44.6s-30.3-17.7-44.6-7.4l-1.6 1.1c-32.1 22.9-76 19.3-103.8-8.6C74 372 74 321 105.5 289.5L217.7 177.2c31.5-31.5 82.5-31.5 114 0c27.9 27.9 31.5 71.8 8.6 103.9l-1.1 1.6c-10.3 14.4-6.9 34.4 7.4 44.6s34.4 6.9 44.6-7.4l1.1-1.6C433.5 260.8 427 182 377 132c-56.5-56.5-148-56.5-204.5 0L60.2 244.3z"/></svg>
`;

const createAnchorElement = function (id, content) {
    const element = document.createElement("a");
    const text = document.createTextNode(content);

    element.href = "#" + id;
    element.classList.add("judgment-body__anchor-link");

    element.appendChild(text);

    return element;
};

const createCopyHelptextElement = function () {
    const element = document.createElement("span");

    element.classList.add("judgment-body__copy-link-helptext");
    element.innerHTML = "Copy link to paragraph";

    return element;
};

const createCopyElement = function (textToCopy) {
    const element = document.createElement("span");
    const helptext = createCopyHelptextElement();

    element.classList.add("judgment-body__copy-link");
    element.innerHTML = linkSvg;
    element.appendChild(helptext);

    element.addEventListener("click", function (event) {
        event.preventDefault();
        event.stopPropagation();
        navigator.clipboard.writeText(textToCopy);
        helptext.innerHTML = "Copied!";

        setTimeout(() => {
            helptext.innerHTML = "Copy link to paragraph";
        }, 3000);
    });

    return element;
};

const createCopyableAnchorElement = function (id, content) {
    const anchorElement = createAnchorElement(id, content);
    const copyElement = createCopyElement(anchorElement.href);

    anchorElement.append(copyElement);

    return anchorElement;
};

const addDocumentParagraphAnchorLinkToSection = function (section) {
    if (!section || !(section instanceof HTMLElement)) return;
    if (!section.hasAttribute("id")) return;

    const sectionId = section.id;

    const numberElement = section.querySelector(".judgment-body__number");

    if (!numberElement) return;

    const numberContent = numberElement.textContent;
    numberElement.innerHTML = "";

    const copyableAnchorElement = createCopyableAnchorElement(
        sectionId,
        numberContent,
    );

    numberElement.appendChild(copyableAnchorElement);
};

const setupDocumentParagraphIconAnchors = function () {
    if (
        !window.waffleFlags ||
        !window.waffleFlags.document_paragraph_icon_anchors
    )
        return;

    const sections = document.querySelectorAll(".judgment-body__section");

    sections.forEach(function (section) {
        addDocumentParagraphAnchorLinkToSection(section);
    });
};

document.addEventListener(
    "DOMContentLoaded",
    setupDocumentParagraphIconAnchors,
);