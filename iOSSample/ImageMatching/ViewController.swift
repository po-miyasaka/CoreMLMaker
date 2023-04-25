
import UIKit
import AVFoundation
import Vision.VNCoreMLRequest
import Photos


class ViewController: UIViewController, AVCaptureVideoDataOutputSampleBufferDelegate{
    
    private var captureSession: AVCaptureSession?
    
    let resultLabel: UILabel = {
        let label = UILabel()
        label.textAlignment = .center
        label.textColor = .white
        label.font = UIFont.systemFont(ofSize: 20)
        label.numberOfLines = 2
        label.translatesAutoresizingMaskIntoConstraints = false
        return label
    }()
    
    override func viewDidAppear(_ animated: Bool) {
        super.viewDidAppear(animated)
        setupCaptureSession()
    }
    
    func setupCaptureSession() {
        captureSession = AVCaptureSession()
        captureSession?.sessionPreset = .photo
        
        guard let backCamera = AVCaptureDevice.default(.builtInWideAngleCamera, for: .video, position: .back),
              let input = try? AVCaptureDeviceInput(device: backCamera),
              captureSession?.canAddInput(input) == true else {
            fatalError("Cannot set up camera input")
        }
        
        captureSession?.addInput(input)
        
        let videoOutput = AVCaptureVideoDataOutput()
        videoOutput.videoSettings = [(kCVPixelBufferPixelFormatTypeKey as String): kCVPixelFormatType_32BGRA]
        videoOutput.setSampleBufferDelegate(self, queue: DispatchQueue(label: "videoQueue"))
        videoOutput.alwaysDiscardsLateVideoFrames = true
        
        guard captureSession?.canAddOutput(videoOutput) == true else {
            fatalError("Cannot set up camera output")
        }
        captureSession?.addOutput(videoOutput)
        
        DispatchQueue.main.async {
            let cameraPreviewLayer = AVCaptureVideoPreviewLayer(session: self.captureSession!)
            cameraPreviewLayer.videoGravity = .resizeAspectFill
            cameraPreviewLayer.frame = self.view.layer.bounds
            self.view.layer.addSublayer(cameraPreviewLayer)
            self.view.addSubview(self.resultLabel)
            NSLayoutConstraint.activate([
                self.resultLabel.centerXAnchor.constraint(equalTo: self.view.centerXAnchor),
                self.resultLabel.bottomAnchor.constraint(equalTo: self.view.safeAreaLayoutGuide.bottomAnchor, constant: -100)
            ])
            
        }
        
        DispatchQueue.global().async { [weak self] in
            self?.captureSession?.startRunning()
        }
    }
    
    func captureOutput(_ output: AVCaptureOutput, didOutput sampleBuffer: CMSampleBuffer, from connection: AVCaptureConnection) {
        guard let pixelBuffer = CMSampleBufferGetImageBuffer(sampleBuffer) else { return }
        let ciImage = CIImage(cvPixelBuffer: pixelBuffer)
        let context = CIContext()
        guard let cgImage = context.createCGImage(ciImage, from: ciImage.extent) else { return }
        let capturedImage = UIImage(cgImage: cgImage)
        
        performImageMatching(capturedImage: capturedImage)
    }
    
    let classifierModel = ImageClassifier().model
    func performImageMatching(capturedImage: UIImage) {
        
        guard let model = try? VNCoreMLModel(for: classifierModel) else {
            fatalError("Failed to load ImageClassifier.mlmodel")
        }
        let request = VNCoreMLRequest(model: model) { (request, error) in
            guard let results = request.results as? [VNClassificationObservation] else {
                fatalError("Failed to process request")
            }
            
            // 処理結果を使って画像マッチングを実行する
            // 例: 最も高い信頼度を持つラベルを取得
            if let bestMatch = results.first {
                DispatchQueue.main.async {
                    self.resultLabel.text = "\(bestMatch.identifier) \nConfidence: \(bestMatch.confidence)"
                    print("Best match: \(bestMatch.identifier) with confidence \(bestMatch.confidence)")
                }
                
            }
        }
        
        if let image = normalizeImage(image: resizeImage(image: capturedImage))?.cgImage {
            try? VNImageRequestHandler(cgImage: image).perform([request])
        }
        
        
    }
    
    let newSize = CGSize(width: 299, height: 299)
    func resizeImage(image: UIImage) -> UIImage {
        
        let renderer = UIGraphicsImageRenderer(size: newSize)
        let resizedImage = renderer.image { _ in
            image.draw(in: CGRect(origin: CGPoint.zero, size: newSize))
        }
        return resizedImage
    }
    
    func normalizeImage(image: UIImage) -> UIImage? {
        return image
        guard let cgImage = image.cgImage else { return nil }
        
        let width = cgImage.width
        let height = cgImage.height
        let colorSpace = CGColorSpaceCreateDeviceRGB()
        let bitmapInfo: UInt32 = CGBitmapInfo.byteOrder32Little.rawValue | CGImageAlphaInfo.premultipliedFirst.rawValue
        
        guard let context = CGContext(data: nil, width: width, height: height, bitsPerComponent: 8, bytesPerRow: 0, space: colorSpace, bitmapInfo: bitmapInfo) else { return nil }
        
        context.draw(cgImage, in: CGRect(x: 0, y: 0, width: width, height: height))
        
        guard let data = context.data else { return nil }
        let rawData = UnsafeMutableRawPointer(data)
        
        for i in 0..<(width * height) {
            let pixel = rawData.load(fromByteOffset: i * 4, as: UInt32.self)
            let r = CGFloat((pixel & 0x0000FF00) >> 8) / 255.0
            let g = CGFloat((pixel & 0x00FF0000) >> 16) / 255.0
            let b = CGFloat((pixel & 0xFF000000) >> 24) / 255.0
            
            let normalizedR = UInt8(r * 255)
            let normalizedG = UInt8(g * 255)
            let normalizedB = UInt8(b * 255)
            
            let normalizedPixel: UInt32 = (UInt32(normalizedB) << 24) | (UInt32(normalizedG) << 16) | (UInt32(normalizedR) << 8) | (pixel & 0x000000FF)
            rawData.storeBytes(of: normalizedPixel, toByteOffset: i * 4, as: UInt32.self)
        }
        
        if let newCgImage = context.makeImage() {
            let newImage = UIImage(cgImage: newCgImage, scale: image.scale, orientation: image.imageOrientation)
            return newImage
        } else {
            return nil
        }
    }
    
}
