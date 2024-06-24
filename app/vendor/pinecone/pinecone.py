import os
from typing import Union, List
from pinecone.grpc import PineconeGRPC as Pinecone, Vector as NonGRPCVector
from pinecone.core.grpc.protos.vector_service_pb2 import Vector as GRPCVector


class PineconeService:
    def __init__(self):
        self.client = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))

    async def upsert(
        self,
        vectors: Union[List[GRPCVector], List[NonGRPCVector], List[tuple], List[dict]],
    ):
        index = self.client.Index("test-1")

        res = index.upsert(
            vectors,
            namespace="fastapi-test",
        )

        return res
