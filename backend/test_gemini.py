import os
import google.generativeai as genai
from dotenv import load_dotenv
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

# 配置Google Gemini API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    logger.error("GOOGLE_API_KEY not found in environment variables")
    raise ValueError("GOOGLE_API_KEY is required")

# 配置Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

def test_gemini_models():
    """测试可用的Gemini模型"""
    logger.info("获取可用模型列表...")
    models = genai.list_models()
    for model_info in models:
        logger.info(f"可用模型: {model_info.name}")
    
    # 尝试不同的模型
    test_models = [
        'gemini-1.5-pro',
        'gemini-1.5-flash',
        'models/gemini-1.5-pro',
        'models/gemini-1.5-flash'
    ]
    
    for model_name in test_models:
        try:
            logger.info(f"测试模型: {model_name}")
            model = genai.GenerativeModel(model_name)
            
            # 发送简单的请求
            prompt = "Hello, can you hear me? Please respond with a simple 'Yes, I can hear you.'"
            response = model.generate_content(prompt)
            
            logger.info(f"模型 {model_name} 测试成功!")
            logger.info(f"响应: {response.text[:100]}...")
            
            return model_name  # 返回成功的模型名称
        except Exception as e:
            logger.error(f"模型 {model_name} 测试失败: {str(e)}")
    
    return None  # 所有模型都失败

if __name__ == "__main__":
    working_model = test_gemini_models()
    if working_model:
        logger.info(f"找到工作的模型: {working_model}")
        
        # 使用工作的模型发送更复杂的请求
        model = genai.GenerativeModel(working_model)
        complex_prompt = """
        请生成一个简短的JSON格式面试问题列表，包含:
        1. 一个技术问题
        2. 一个行为问题
        
        要求以JSON格式返回，结构为:
        {
            "technical_question": "问题内容",
            "behavioral_question": "问题内容"
        }
        """
        
        try:
            response = model.generate_content(complex_prompt)
            logger.info(f"复杂请求响应: {response.text}")
        except Exception as e:
            logger.error(f"复杂请求失败: {str(e)}")
    else:
        logger.error("没有找到可工作的Gemini模型") 