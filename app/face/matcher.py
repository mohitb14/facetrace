import numpy as np


class FaceMatcher:

    def cosine_similarity(self, embedding1, embedding2):

        embedding1 = np.array(embedding1)
        embedding2 = np.array(embedding2)

        dot_product = np.dot(
            embedding1,
            embedding2
        )

        norm1 = np.linalg.norm(
            embedding1
        )

        norm2 = np.linalg.norm(
            embedding2
        )

        if norm1 == 0 or norm2 == 0:
            return 0.0

        similarity = (
            dot_product /
            (norm1 * norm2)
        )

        return float(similarity)

    def compare(self, face1, face2):

        return self.cosine_similarity(
            face1.embedding,
            face2.embedding
        )