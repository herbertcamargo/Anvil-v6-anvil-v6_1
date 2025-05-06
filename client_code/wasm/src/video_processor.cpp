#include <emscripten/emscripten.h>
#include <emscripten/bind.h>
#include <cstdint>
#include <vector>

// Simple video processing class
class VideoProcessor {
public:
    // Apply grayscale effect to image data (RGBA format)
    void applyGrayscale(uint8_t* data, int width, int height) {
        int size = width * height * 4; // RGBA format (4 bytes per pixel)
        for (int i = 0; i < size; i += 4) {
            // Calculate grayscale using luminance formula
            uint8_t gray = static_cast<uint8_t>(
                0.299 * data[i] +     // R
                0.587 * data[i + 1] + // G
                0.114 * data[i + 2]   // B
            );
            
            // Set RGB channels to gray value (keep alpha unchanged)
            data[i] = gray;     // R
            data[i + 1] = gray; // G
            data[i + 2] = gray; // B
            // data[i + 3] unchanged (alpha)
        }
    }

    // Apply sepia tone effect
    void applySepia(uint8_t* data, int width, int height) {
        int size = width * height * 4;
        for (int i = 0; i < size; i += 4) {
            uint8_t r = data[i];
            uint8_t g = data[i + 1];
            uint8_t b = data[i + 2];
            
            // Sepia formula
            int newR = static_cast<int>(0.393 * r + 0.769 * g + 0.189 * b);
            int newG = static_cast<int>(0.349 * r + 0.686 * g + 0.168 * b);
            int newB = static_cast<int>(0.272 * r + 0.534 * g + 0.131 * b);
            
            // Clamp values to 0-255
            data[i] = (newR > 255) ? 255 : static_cast<uint8_t>(newR);
            data[i + 1] = (newG > 255) ? 255 : static_cast<uint8_t>(newG);
            data[i + 2] = (newB > 255) ? 255 : static_cast<uint8_t>(newB);
            // data[i + 3] unchanged (alpha)
        }
    }
    
    // Apply brightness adjustment
    void adjustBrightness(uint8_t* data, int width, int height, float factor) {
        int size = width * height * 4;
        for (int i = 0; i < size; i += 4) {
            // Apply brightness factor to RGB channels
            for (int j = 0; j < 3; j++) {
                int newValue = static_cast<int>(data[i + j] * factor);
                data[i + j] = (newValue > 255) ? 255 : 
                              (newValue < 0) ? 0 : static_cast<uint8_t>(newValue);
            }
            // data[i + 3] unchanged (alpha)
        }
    }
    
    // Apply blur effect (simple box blur)
    void applyBlur(uint8_t* data, int width, int height, int radius) {
        // Create a copy of the original data
        std::vector<uint8_t> originalData(data, data + width * height * 4);
        
        // Apply box blur
        for (int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                int r = 0, g = 0, b = 0, a = 0;
                int count = 0;
                
                // Sum up pixel values in the radius
                for (int ky = -radius; ky <= radius; ky++) {
                    for (int kx = -radius; kx <= radius; kx++) {
                        int posX = x + kx;
                        int posY = y + ky;
                        
                        if (posX >= 0 && posX < width && posY >= 0 && posY < height) {
                            int index = (posY * width + posX) * 4;
                            r += originalData[index];
                            g += originalData[index + 1];
                            b += originalData[index + 2];
                            a += originalData[index + 3];
                            count++;
                        }
                    }
                }
                
                // Calculate average and set new values
                int index = (y * width + x) * 4;
                data[index] = static_cast<uint8_t>(r / count);
                data[index + 1] = static_cast<uint8_t>(g / count);
                data[index + 2] = static_cast<uint8_t>(b / count);
                data[index + 3] = static_cast<uint8_t>(a / count);
            }
        }
    }
};

// Function to process video frame
extern "C" {
    EMSCRIPTEN_KEEPALIVE
    void processVideoFrame(uint8_t* data, int width, int height, int effectType, float param) {
        VideoProcessor processor;
        
        switch (effectType) {
            case 0: // Grayscale
                processor.applyGrayscale(data, width, height);
                break;
            case 1: // Sepia
                processor.applySepia(data, width, height);
                break;
            case 2: // Brightness
                processor.adjustBrightness(data, width, height, param);
                break;
            case 3: // Blur
                processor.applyBlur(data, width, height, static_cast<int>(param));
                break;
            default:
                break;
        }
    }
}

// Use embind to expose the VideoProcessor class to JavaScript
EMSCRIPTEN_BINDINGS(video_processor_module) {
    emscripten::class_<VideoProcessor>("VideoProcessor")
        .constructor<>()
        .function("applyGrayscale", &VideoProcessor::applyGrayscale)
        .function("applySepia", &VideoProcessor::applySepia)
        .function("adjustBrightness", &VideoProcessor::adjustBrightness)
        .function("applyBlur", &VideoProcessor::applyBlur);
} 