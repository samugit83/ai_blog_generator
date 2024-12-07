from langchain.chains import LLMChain, TransformChain, SequentialChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI  # Updated import
from huggingface_hub import InferenceClient
import re
from datetime import datetime
import os
from PIL import Image
from dotenv import load_dotenv 
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
if not HUGGINGFACE_API_TOKEN:
    raise ValueError("Hugging Face API token not found. Please set the HUGGINGFACE_API_TOKEN environment variable.")

llm_a = ChatOpenAI(model="gpt-4o", temperature=0.7, openai_api_key=OPENAI_API_KEY)
llm_c = ChatOpenAI(model="gpt-4o", temperature=0.8, openai_api_key=OPENAI_API_KEY)

# Chain A: Extract latest 5 hot trends
prompt_a = PromptTemplate(
    template="""
    You are an expert trend analyst on {topic}. Please provide the latest {nr_of_articles} hot trends on the internet as of {current_date} on the {topic}. List them as a numbered list.
    """,
    input_variables=["current_date", "topic", "nr_of_articles"]
)


chain_a = LLMChain(
    llm=llm_a,
    prompt=prompt_a,
    output_key="trends_text"
)

# Chain B: Extract relevant information for each trend
def extract_news_info(inputs: dict):
    trends_text = inputs['trends_text']
    current_date = inputs['current_date']
    trends = re.findall(r'\d+\.\s+(.*)', trends_text)
    extracted_info = {}
    for trend in trends:
        # In a real scenario, integrate with news APIs here
        extracted_info[trend] = f"Latest news and updates about {trend} as of {current_date}."
    return {"news_info": extracted_info}

chain_b = TransformChain(
    input_variables=["trends_text", "current_date"],
    output_variables=["news_info"],
    transform=extract_news_info
)

# Chain C: Write blog articles for each trend
prompt_c = PromptTemplate(
    template="""
    You are a professional blogger. Write a detailed and engaging blog article about the following trend using the provided information.

    Trend: {trend}
    Information: {info}
    Language: {language}
    Tone: {tone}

    The article should be suitable for a general audience and approximately {word_count} words.
    """,
    input_variables=["trend", "info", "language", "tone", "word_count"]
)



def write_articles(inputs: dict):
    news_info = inputs['news_info']
    language = inputs['language']
    tone = inputs['tone']
    word_count = inputs['word_count']
    articles = {}
    for trend, info in news_info.items():
        result = prompt_c.format(
            trend=trend, 
            info=info,
            language=language,
            tone=tone,
            word_count=word_count
        )
        article = llm_c.invoke(result)
        articles[trend] = article.content
    return {"articles": articles}



chain_c = TransformChain(
    input_variables=["news_info"],
    output_variables=["articles"],
    transform=write_articles
)

# Chain D: Generate images for each article
def generate_images(inputs: dict):
    articles = inputs['articles']
    print("\n=== Debug: Starting Image Generation ===")
    print(f"Number of articles to process: {len(articles)}")
    
    client = InferenceClient(
        "black-forest-labs/FLUX.1-dev",
        token=HUGGINGFACE_API_TOKEN
    )
    images = {}
    
    for trend, article in articles.items():
        print(f"\nProcessing trend: {trend}")
        first_sentence = article.split('.')[0]
        prompt = first_sentence if first_sentence else "An illustration for a blog article."
        
        try:
            print(f"Using prompt: {prompt}")

            image = client.text_to_image(prompt)
            print(f"Image generation response type: {type(image)}")
            
            if isinstance(image, Image.Image):
                print("Successfully received PIL Image")
                images[trend] = image
            else:
                print(f"Unexpected response format: {type(image)}")
                
        except Exception as e:
            print(f"Error in image generation: {str(e)}")
            images[trend] = None
    
    print("\n=== Debug: Finished Image Generation ===")
    return {"images": images}


chain_d = TransformChain(
    input_variables=["articles"],
    output_variables=["images"],
    transform=generate_images
)


full_chain = SequentialChain(
    chains=[chain_a, chain_b, chain_c, chain_d],
    input_variables=["current_date", "topic", "language", "tone", "word_count", "nr_of_articles"],
    output_variables=["current_date", "trends_text", "news_info", "articles", "images"],
    verbose=True
)


def execute_workflow():
    current_date = datetime.now().strftime("%Y-%m-%d")
    print("\n=== Debug: Starting Workflow ===")
    
    # Run the full chain
    result = full_chain.invoke({
        "current_date": current_date,
        "topic": "IT field",
        "language": "English",
        "tone": "informative and engaging",
        "word_count": 800,
        "nr_of_articles": 1
    })

    output_dir = "/app/output"
    print(f"\nChecking output directory: {output_dir}")
    try:
        os.makedirs(output_dir, exist_ok=True)
        print(f"Output directory exists or was created: {os.path.exists(output_dir)}")
        print(f"Directory permissions: {oct(os.stat(output_dir).st_mode)[-3:]}")
    except Exception as e:
        print(f"Error with output directory: {str(e)}")

    images = result.get("images", {})
    print(f'\nNumber of images to save: {len(images)}')
    
    for idx, (trend, image) in enumerate(images.items(), 1):
        print(f"\nProcessing image {idx} for trend: {trend}")
        if image:
            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                image_path = os.path.join(output_dir, f"trend_{idx}_{timestamp}.jpg")
                image.save(image_path)
                print(f"Image saved successfully at: {image_path}")
            except Exception as e:
                print(f"Error saving image: {str(e)}")
        else:
            print(f"No image object available for trend {idx}")


if __name__ == "__main__":
    execute_workflow()
