from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base
from pydantic import Field

mcp = FastMCP("DocumentMCP")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": (
        "These financials outline the project's budget and expenditures."
    ),
    "outlook.pdf": (
        "This document presents the projected future performance of the system."
    ),
    "plan.md": ("The plan outlines the steps for the project's implementation."),
    "spec.txt": (
        "These specifications define the technical requirements for the equipment."
    ),
}


# TOOLS #


@mcp.tool(
    name="read_doc_contents",
    description=(
        "Read the contents of the provided document and return the contents as a string"
    ),
)
def read_doc(doc_id: str = Field(description="Id of the document to read.")) -> str:
    if doc_id not in docs:
        raise ValueError(f"Document with id {doc_id} not found.")

    return docs[doc_id]


@mcp.tool(
    name="edit_doc_contents",
    description=(
        "Edits a document by replacing an exisiting substring with a new substring."
    ),
)
def edit_doc(
    doc_id: str = Field(description="Id of the document to edit."),
    exisiting_substring: str = Field(
        description="A substring in the document to replace. Must match exactly."
    ),
    new_substring: str = Field(
        description="A substring to replace the existing_substring with."
    ),
) -> str:
    if doc_id not in docs:
        raise ValueError(f"Document with id {doc_id} not found.")

    edited_doc = docs[doc_id].replace(exisiting_substring, new_substring)
    docs[doc_id] = edited_doc
    return edited_doc


# RESOURCES #


@mcp.resource("docs://documents", mime_type="application/json")
def get_doc_ids() -> list[str]:
    return list(docs.keys())


@mcp.resource("docs://documents/{doc_id}", mime_type="text/plain")
def get_doc(doc_id: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Document with id: {doc_id} not found.")

    return docs[doc_id]


# PROMPTS #


@mcp.prompt(
    name="format", description="Returns the contents of a document in markdown format"
)
def format_doc_to_mkdwn(
    doc_id=Field(description="Id of the document to convert to markdown."),
) -> list[base.Message]:
    prompt = f"""
    Your goal is to reformat a document to be written with markdown syntax.
    The id of the document you need to reformat is:

    <document_id>
    {doc_id}
    </document_id>

    Add in headers, bullet points, tables, etc as necessary.
    use the "edit_document" tool to edit the document.
    """
    return [base.UserMessage(prompt)]


@mcp.prompt(
    name="summarize", description="Provides three keywords the summarize a document."
)
def summarize_document(
    doc_id=Field(description="Id of the document to summarize."),
) -> list[base.Message]:
    prompt = f"""
    Your goal is to summarize a document down to three keywords.
    the id of the document you need to summarize is:

    <document_id>
    {doc_id}
    </document_id>

    Use the "summarize_doc tool to summarize the document.

    """
    return [base.UserMessage(prompt)]


if __name__ == "__main__":
    mcp.run(transport="stdio")
