from mcp.server.fastmcp import FastMCP
from pydantic import Field

mcp = FastMCP("DocumentMCP")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}


@mcp.tool(
    name="read_doc_contents",
    description="Read the contents of the provided document and return the contents as a string"
)
def read_doc(
    doc_id: str = Field(description="Id of the document to read.")
) -> str:
    if doc_id not in docs:
        raise ValueError(f"Document with id {doc_id} not found.")

    return docs[doc_id]


@mcp.tool(
    name="edit_doc_contents",
    description="Edits a document by replacing an exisiting substring with a new substring."
)
def edit_doc(
    doc_id: str = Field(description="Id of the document to edit."),
    exisiting_substring: str = Field(
        description="A substring in the document to replace. Must match exactly."),
    new_substring: str = Field(
        description="A substring to replace the existing_substring with.")
) -> str:
    if doc_id not in docs:
        raise ValueError(f"Document with id {doc_id} not found.")

    edited_doc = docs[doc_id].replace(exisiting_substring, new_substring)
    docs[doc_id] = edited_doc
    return edited_doc


    # TODO: Write a resource to return all doc id's
    # TODO: Write a resource to return the contents of a particular doc
    # TODO: Write a prompt to rewrite a doc in markdown format
    # TODO: Write a prompt to summarize a doc
if __name__ == "__main__":
    mcp.run(transport="stdio")
