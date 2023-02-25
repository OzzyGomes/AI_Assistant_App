import openai

class OpenAIPlayground:
    def __init__(self, api_key):
        self.openai = openai
        self.openai.api_key = api_key

    def send_prompt_request(self, prompt, temperature=0.0, max_tokens=1000, presence_penalty=0.0):
        try:
            response = self.openai.Completion.create(
                model='text-davinci-003',
                prompt=prompt,
                temperature=temperature,
                max_tokens=max_tokens,
                presence_penalty=presence_penalty,
                n=1
            )
            result = {
                'id': response.id,
                'created': response.created,
                'model': response.model,
                'completion_tokens': response.usage.completion_tokens,
                'prompt_tokens' : response.usage.prompt_tokens,
                'total_tokens' : response.usage.total_tokens,
                'outputs' : response.choices[0].text,
                'status' : response.choices[0].finish_reason
            }
            return result
        except Exception as e:
            return {'error' : e}
