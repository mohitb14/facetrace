import insightface


class FaceDetector:

    def __init__(self):
        self.model = insightface.app.FaceAnalysis(
            name="buffalo_l"
        )

        self.model.prepare(
            ctx_id=0,
            det_size=(640, 640)
        )

    def detect(self, image):
        faces = self.model.get(image)
        return faces