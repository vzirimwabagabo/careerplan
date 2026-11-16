from copy import deepcopy
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree

SOURCE = Path(r"C:\Users\USER\Downloads\1773847845240_Worksheet_-_Build_a_Career_Plan.docx")
OUTPUT = Path(r"C:\Users\USER\Desktop\Projects\CareerPlan\deliverables\Valentin-Zirimwabagabo-Career-Plan-Worksheet-Ready.docx")
STAGED = Path(r"C:\Users\USER\Desktop\Projects\CareerPlan\.worksheet_work\filled.docx")
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
XML = "http://www.w3.org/XML/1998/namespace"
Q = lambda name: f"{{{W}}}{name}"

def body_paragraphs(root):
    body = root.find(f".//{Q('body')}")
    return [child for child in body if child.tag == Q("p")]

def normal_run(text, half_points="22"):
    run = etree.Element(Q("r"))
    props = etree.SubElement(run, Q("rPr"))
    bold = etree.SubElement(props, Q("b"))
    bold.set(Q("val"), "0")
    size = etree.SubElement(props, Q("sz"))
    size.set(Q("val"), half_points)
    size_cs = etree.SubElement(props, Q("szCs"))
    size_cs.set(Q("val"), half_points)
    node = etree.SubElement(run, Q("t"))
    node.set(f"{{{XML}}}space", "preserve")
    node.text = text
    return run

def fill_blank(paragraph, value, numbered=False):
    text_nodes = paragraph.xpath("./w:r/w:t", namespaces={"w": W})
    if text_nodes:
        node = text_nodes[-1]
        existing = node.text or ""
        if not existing.strip():
            node.text = (" " if numbered else "") + value
            node.set(f"{{{XML}}}space", "preserve")
        else:
            raise ValueError("Expected a blank paragraph")
        return
    paragraph.append(normal_run((" " if numbered else "") + value))

def replace_existing(paragraph, value):
    nodes = paragraph.xpath("./w:r/w:t", namespaces={"w": W})
    substantive = [node for node in nodes if (node.text or "").strip()]
    if not substantive:
        raise ValueError("Expected existing text")
    substantive[-1].text = value
    for node in substantive[:-1]:
        node.text = ""

def set_heading(paragraph, value):
    nodes = paragraph.xpath("./w:r/w:t", namespaces={"w": W})
    substantive = [node for node in nodes if (node.text or "").strip()]
    substantive[0].text = value
    for node in substantive[1:]:
        node.text = ""

career = {
    4: "Build reliable software and data tools for practical needs; grow toward technical leadership in East Africa.",
    8: "Build two tested software/data projects; strengthen Python, SQL, APIs, and deployment.",
    9: "Secure a junior developer, implementation, or data-operations role or internship.",
    12: "Become a trusted software and data professional who can deliver end to end.",
    13: "Progress toward technical leadership in software/data and community-serving technology.",
}
one_year = [
    "Apply to funded applied AI/data master’s programmes after checking fit, funding, deadlines, and eligibility.",
    "Ship a tested stock/sales tool for Turashoboye Feeds; use synthetic or approved data.",
    "Publish a reproducible Python/SQL analysis of an open dataset.",
    "Review 15 live postings; NISR counted 17,492 information/communication jobs in Rwanda in 2025 (employment, not vacancies; LFS 2025).",
    "Get feedback from three professionals; revise my CV and portfolio.",
]
three_year = [
    "Work in a software, data, or communications company.",
    "Own a feature from user needs through testing and deployment.",
    "Specialise in backend/application development and data quality.",
    "Deliver a documented digital project with a business or community partner.",
    "Decide whether a funded master’s fits my experience and plans.",
]
five_year = [
    "Build the family life I want, including marriage as circumstances allow.",
    "Progress into specialist or mid-level software/data work.",
    "Aim to lead or co-found a useful technology initiative.",
]

with ZipFile(SOURCE, "r") as zin:
    root = etree.fromstring(zin.read("word/document.xml"))
    paragraphs = body_paragraphs(root)
    if len(paragraphs) != 37:
        raise ValueError(f"Unexpected worksheet structure: {len(paragraphs)} paragraphs")
    for index, value in career.items():
        fill_blank(paragraphs[index], value)
    set_heading(paragraphs[19], "One-Year Goals (by Nov 2027):")
    set_heading(paragraphs[26], "Three-Year Goals (by Nov 2029):")
    set_heading(paragraphs[33], "Five-Year Goals (by Nov 2031):")
    replace_existing(paragraphs[20], one_year[0])
    for index, value in zip(range(21, 25), one_year[1:]):
        fill_blank(paragraphs[index], value, numbered=True)
    replace_existing(paragraphs[27], three_year[0])
    for index, value in zip(range(28, 32), three_year[1:]):
        fill_blank(paragraphs[index], value, numbered=True)
    replace_existing(paragraphs[34], five_year[0])
    for index, value in zip(range(35, 37), five_year[1:]):
        fill_blank(paragraphs[index], value, numbered=True)

    # The original response block contains one empty spacer after its final
    # divider; remove it so the completed goals remain on the worksheet's page.
    body = root.find(f".//{Q('body')}")
    body.remove(paragraphs[15])

    xml_bytes = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)
    with ZipFile(STAGED, "w", compression=ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = xml_bytes if item.filename == "word/document.xml" else zin.read(item.filename)
            zout.writestr(item, data)

if OUTPUT.exists():
    raise FileExistsError(f"Refusing to overwrite {OUTPUT}")
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_bytes(STAGED.read_bytes())
print(OUTPUT)
