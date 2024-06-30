import os
from typing import Union, List
from pinecone.grpc import PineconeGRPC as Pinecone, Vector as NonGRPCVector
from pinecone.core.grpc.protos.vector_service_pb2 import Vector as GRPCVector


class PineconeService:
    def __init__(self):
        self.client = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
        self.index = self.client.Index("test-1")

    # index.upsert([{'id': 'id1', 'values': [1.0, 2.0, 3.0], 'metadata': {'key': 'value'}},
    async def upsert(
        self,
        vectors: Union[List[GRPCVector], List[NonGRPCVector], List[tuple], List[dict]],
    ):
        # TODO: probably use env vars for the namespace and index name 

        return self.index.upsert(
            vectors,
            namespace="cocktails",
        )

    async def query(self, vectors: List[float]):
        return self.index.query(
            namespace="cocktails",
            vector=vectors,
            top_k=3
        )
