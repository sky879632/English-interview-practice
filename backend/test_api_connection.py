#!/usr/bin/env python3
"""
检查API连接和环境变量的测试脚本
用法: python test_api_connection.py
"""

import os
import sys
from dotenv import load_dotenv

def check_env_files():
    """检查.env文件是否正确设置"""
    print("==== 检查环境变量文件 ====")
    
    # 检查.env.example
    if os.path.exists('.env.example'):
        print("✅ .env.example文件存在")
    else:
        print("❌ .env.example文件不存在，请创建")
    
    # 检查.env
    if os.path.exists('.env'):
        print("✅ .env文件存在")
    else:
        print("⚠️ .env文件不存在，请从.env.example复制一份")
        return False
    
    # 检查.env是否被git忽略
    if os.path.exists('.git'):
        import subprocess
        try:
            result = subprocess.run(['git', 'check-ignore', '-v', '.env'], 
                                    capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ .env文件已被git正确忽略")
            else:
                print("⚠️ .env文件可能没有被git忽略。检查.gitignore配置")
        except Exception as e:
            print(f"⚠️ 无法检查git忽略状态: {e}")
    
    return True

def check_api_key():
    """检查API密钥是否已设置"""
    print("\n==== 检查API密钥 ====")
    
    # 加载环境变量
    load_dotenv()
    
    # 检查API密钥
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ GOOGLE_API_KEY未设置，请在.env文件中设置")
        return False
    
    if api_key == "your_api_key_here":
        print("❌ GOOGLE_API_KEY仍然是默认值，请修改为真实密钥")
        return False
    
    # 屏蔽显示真实密钥
    masked_key = api_key[:4] + '*' * (len(api_key) - 8) + api_key[-4:]
    print(f"✅ GOOGLE_API_KEY已设置: {masked_key}")
    return True

def test_api_connection():
    """测试API连接"""
    print("\n==== 测试API连接 ====")
    
    try:
        import google.generativeai as genai
        
        # 配置API
        api_key = os.getenv('GOOGLE_API_KEY')
        genai.configure(api_key=api_key)
        
        # 获取模型列表
        models = genai.list_models()
        print(f"✅ 成功连接API并获取模型列表")
        print(f"✅ 可用模型数量: {len(models)}")
        
        # 测试简单请求
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content("Hello world!")
        
        print("✅ API请求测试成功")
        print(f"响应: {response.text}")
        return True
        
    except ImportError:
        print("❌ 未安装google-generativeai库，请运行: pip install google-generativeai")
        return False
    except Exception as e:
        print(f"❌ API连接测试失败: {e}")
        return False

if __name__ == "__main__":
    print("Google Gemini API连接测试工具")
    print("----------------------------")
    
    env_ok = check_env_files()
    if not env_ok:
        print("\n❌ 环境文件检查失败，请修复上述问题")
        sys.exit(1)
    
    key_ok = check_api_key()
    if not key_ok:
        print("\n❌ API密钥检查失败，请修复上述问题")
        sys.exit(1)
    
    connection_ok = test_api_connection()
    if not connection_ok:
        print("\n❌ API连接测试失败，请修复上述问题")
        sys.exit(1)
    
    print("\n✅ 所有检查通过，API连接正常")
    print("可以继续开发和使用应用程序")
    sys.exit(0) 