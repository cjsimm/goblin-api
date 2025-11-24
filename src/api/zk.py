from fastapi import APIRouter, Response

zk = APIRouter(prefix="/zk")


@zk.post("/fleeting")
async def create() -> Response:
    """
    Create a fleeting zk note and add it to an obsidian vault in the unsorted category
    """
    return Response()
