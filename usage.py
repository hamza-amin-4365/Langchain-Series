from imageProcessing import ProcessQuery

def getImages(state):
    query = state["imageQuery"]
    result = ProcessQuery(query)
    
    print("\n" + "="*50)
    print(f"Query: {query}")
    print("="*50)
    
    if result['image_path']:
        print(f"Image downloaded: {result['image_path']}")
        print("\nCaption:")
        print(result['caption'])
    else:
        print(result['caption'])  # This will be the error message if no image was found
    
    print("="*50 + "\n")

# Example usage:
state = {
    "imageQuery": "What is the map of the Roman Empire"
}
getImages(state)