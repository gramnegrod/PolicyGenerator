Developer Quickstart: Using OpenAI's API

1. Setup
a. Create and Export API Key

Generate an API key from the OpenAI Dashboard.
Store it securely (e.g., .env file).
Export as an environment variable:
export OPENAI_API_KEY="your_api_key_here"
b. Install OpenAI SDK

For Node.js:
npm install openai
2. Making Your First API Request
a. Text Generation with Chat Completions

Example: Generate a Haiku
import OpenAI from "openai";

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

const response = await openai.chat.completions.create({
  model: "gpt-4o",
  messages: [
    { role: "system", content: "You are a helpful assistant." },
    { role: "user", content: "Write a haiku about recursion in programming." },
  ],
});

console.log(response.choices[0].message.content);
3. Key Features and Endpoints
a. Chat Completions

Purpose: Generate human-like text responses.
Usage: Define system, user, and optionally assistant messages.
Models: gpt-4o, gpt-4o-mini, o1-preview, o1-mini.
b. Image Generation (DALL·E)

Create Images:
const image = await openai.images.generate({
  model: "dall-e-3",
  prompt: "a white siamese cat",
  size: "1024x1024",
  quality: "standard",
  n: 1,
});
console.log(image.data[0].url);
Edit Images (DALL·E 2):
const editedImage = await openai.images.edit({
  model: "dall-e-2",
  image: fs.createReadStream("sunlit_lounge.png"),
  mask: fs.createReadStream("mask.png"),
  prompt: "A sunlit indoor lounge area with a pool containing a flamingo",
  n: 1,
  size: "1024x1024",
});
console.log(editedImage.data[0].url);
c. Vision (GPT-4 with Vision)

Analyze Images:
const visionResponse = await openai.chat.completions.create({
  model: "gpt-4o-mini",
  messages: [
    { role: "user", content: "What’s in this image?" },
    { type: "image_url", image_url: { url: "https://example.com/image.jpg" } },
  ],
  max_tokens: 300,
});
console.log(visionResponse.choices[0].message.content);
d. Audio Generation

Text-to-Speech:
response = openai.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input="Today is a wonderful day to build something people love!"
)
with open("speech.mp3", "wb") as f:
    f.write(response.audio.data)
Speech-to-Text:
transcription = openai.audio.transcriptions.create(
    model="whisper-1",
    file=open("/path/to/audio.mp3", "rb")
)
print(transcription.text)
4. Advanced Features
a. Function Calling

Define Functions:
const tools = [
  {
    type: "function",
    function: {
      name: "get_weather",
      description: "Get the weather for a location.",
      parameters: {
        type: "object",
        properties: {
          location: { type: "string" },
          unit: { type: "string", enum: ["c", "f"] },
        },
        required: ["location", "unit"],
        additionalProperties: false,
      },
    },
  },
];
Invoke Function:
const response = await openai.chat.completions.create({
  model: "gpt-4o",
  messages: [{ role: "user", content: "What's the weather in Paris today?" }],
  tools: tools,
});
if (response.choices[0].message.tool_calls) {
  const toolCall = response.choices[0].message.tool_calls[0];
  const args = JSON.parse(toolCall.function.arguments);
  const weather = get_weather(args.location, args.unit);
  // Respond with weather info
}
b. Structured Outputs

Define Schema:
const CalendarEvent = {
  type: "object",
  properties: {
    name: { type: "string" },
    date: { type: "string" },
    participants: { type: "array", items: { type: "string" } },
  },
  required: ["name", "date", "participants"],
  additionalProperties: false,
};

const response = await openai.chat.completions.create({
  model: "gpt-4o-2024-08-06",
  messages: [
    { role: "system", content: "Extract the event information." },
    { role: "user", content: "Alice and Bob are going to a science fair on Friday." },
  ],
  response_format: { type: "json_schema", json_schema: CalendarEvent },
});

const event = response.choices[0].message.parsed;
c. Batch API

Prepare Batch File (batchinput.jsonl):
{"custom_id": "req-1", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "gpt-4o", "messages": [{"role": "user", "content": "Hello world!"}], "max_tokens": 1000}}
{"custom_id": "req-2", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "gpt-4o", "messages": [{"role": "user", "content": "Goodbye world!"}], "max_tokens": 1000}}
Upload and Create Batch:
const batchFile = await openai.files.create({
  file: fs.createReadStream("batchinput.jsonl"),
  purpose: "batch",
});

const batch = await openai.batches.create({
  input_file_id: batchFile.id,
  endpoint: "/v1/chat/completions",
  completion_window: "24h",
  metadata: { description: "Nightly eval job" },
});

// Check status and retrieve results
const status = await openai.batches.retrieve(batch.id);
if (status.status === "completed") {
  const results = await openai.files.content(status.output_file_id);
  console.log(results.text);
}
5. Fine-Tuning
a. Prepare Dataset (fine_tune.jsonl):

{"messages": [{"role": "system", "content": "You are a sarcastic assistant."}, {"role": "user", "content": "What's the capital of France?"}, {"role": "assistant", "content": "Paris, obviously."}]}
b. Upload and Create Fine-Tune Job:

const fineTuneFile = await openai.files.create({
  file: fs.createReadStream("fine_tune.jsonl"),
  purpose: "fine-tune",
});

const fineTuneJob = await openai.fine_tuning.jobs.create({
  training_file: fineTuneFile.id,
  model: "gpt-4o-mini-2024-07-18",
  n_epochs: 2,
});

// Monitor and use the fine-tuned model
const fineTunedModel = fineTuneJob.fine_tuned_model;
const response = await openai.chat.completions.create({
  model: fineTunedModel,
  messages: [{ role: "user", content: "Tell me a joke." }],
});
console.log(response.choices[0].message.content);
6. Function Calling Best Practices
Define clear, descriptive function and parameter names.
Limit the number of functions (recommended ≤20).
Use enums to constrain parameter values.
Enable Structured Outputs (strict: true) for schema adherence.
Handle edge cases and errors gracefully in your implementation.
7. Additional Resources
OpenAI Documentation
OpenAI Cookbook
API Reference
Playground
Summary
This concise guide provides the essential steps and code snippets to help an AI understand how to interact with OpenAI's API using the new chat completions syntax. It covers setup, making requests, key features (like text and image generation, audio processing), advanced functionalities (function calling, structured outputs, batch processing), and fine-tuning. Additionally, it highlights best practices and points to further resources for in-depth exploration.

If you need further refinements or additional sections condensed, feel free to let me know!