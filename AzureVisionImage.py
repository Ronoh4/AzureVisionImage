import os
from dotenv import load_dotenv
import sys 
import azure.ai.vision as sdk

def main():
    try:
        # Get Configuration Settings and Authenticate Client
        load_dotenv()
        ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        ai_key = os.getenv('AI_SERVICE_KEY')
        cv_client = sdk.ComputerVisionClient(endpoint=ai_endpoint, credential=sdk.KeyCredential(ai_key))

        # Get & Analyze image
        image_file = 'images/street.jpg'
        if len(sys.argv) > 1: 
            image_file = sys.argv[1]
        AnalyzeImage(image_file, cv_client)

    except Exception as ex:
        print(ex)

def AnalyzeImage(image_file, cv_client):
    print('\nAnalyzing', image_file)

    # Specify features to be retrieved
    analysis_options = sdk.ImageAnalysisOptions(
        features=[
            sdk.ImageAnalysisFeature.CAPTION,
            sdk.ImageAnalysisFeature.TAGS,
            sdk.ImageAnalysisFeature.OBJECTS
        ]
    )
    # Get image analysis
    image = sdk.VisionSource(image_file)
    image_analyzer = sdk.ImageAnalyzer(cv_client, image, analysis_options)
    result = image_analyzer.analyze()

if result.reason == sdk.ImageAnalysisResultReason.ANALYZED:

    # Access and display image captions
    if result.captions:
        print("\nCaptions:")
        for caption in result.captions:
            print(f"Caption: '{caption.text}' (confidence: {caption.confidence * 100:.2f}%)")


    # Access and display tags
    if result.tags:
        print("\nTags:")
        for tag in result.tags:
            print(f"Tag: '{tag.name}' (confidence: {tag.confidence * 100:.2f}%)")

    # Access and display objects
    if result.objects:
        print("\nObjects:")
        for obj in result.objects:
            print(f"Object: '{obj.object_property}' (confidence: {obj.confidence * 100:.2f}%)")

else:
    # Handle analysis errors
    error_details = sdk.ImageAnalysisErrorDetails.from_result(result)
    print("Analysis failed.")
    print(f"Error reason: {error_details.reason}")
    print(f"Error code: {error_details.error_code}")
    print(f"Error message: {error_details.message}")


if __name__ == "__main__":
   main()
