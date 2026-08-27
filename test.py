import onnx
model = onnx.load("src/model/face_detection_yunet_2026may.onnx")
onnx.checker.check_model(model)
print("Model is valid!")
