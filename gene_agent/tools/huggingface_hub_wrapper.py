import os
import dspy

class HuggingFaceTextGenerationLM(dspy.LM):
    def __init__(self, client, model, **kwargs):
        self.client = client
        self.model = model
        self.kwargs = kwargs

    def _request(self, prompt, **kwargs):
        response = self.client.text_generation(
            model=self.model,
            prompt=prompt,
            **self.kwargs,
            **kwargs
        )
        return [response]
    
    def __call__(self, messages, **kwargs):
        return self._request(messages, **kwargs)

class HuggingFaceChatCompletionLM(dspy.LM):
    def __init__(self, client, model, **kwargs):
        self.client = client
        self.model = model
        self.kwargs = kwargs
        self.index = 0
        self.called = 0
        self.call = 0

    def _request(self, prompt, **kwargs):
        # print("---"*20)
        # print(prompt)
        # print("---"*20)
        try:
            self.index += 1
            response = self.client.chat.completions.create(
                model=self.model,
                messages=prompt,
                **self.kwargs,
                **kwargs
            )
            print(f"{self.index}---"*20)
            print(response)
            print("---"*20)
            self.called = 0
            return [{'text': response.choices[0].message.content}]
        except Exception as e:
                return [{'text': ''}]

    def __call__(self, messages, **kwargs):
        if self.called:
            return
        self.called = 1
        self.call += 1
        print(f"{self.call}---"*20)
        print(messages)
        print("---"*20)
        return self._request(messages, **kwargs)
