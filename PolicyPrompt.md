Here's a comprehensive plan for implementing the Policy & Procedure Generator card to replace the Podcast Summary slot. This feature will help
  users convert spoken ideas into structured policy documents using the specialized healthcare management prompt.

  Feature Overview

  The Policy & Procedure Generator will allow healthcare professionals to dictate rough concepts for medical office policies and procedures, which
   will then be transformed into well-structured, compliant documents following industry standards. The workflow will mirror the current
  transcription process but with specialized processing for policy documents.

  Implementation Requirements

  1. Dashboard Card Update
    - Replace the "Podcast Summaries" card with "Policy & Procedure Generator"
    - Update the description to explain the purpose of converting spoken policy ideas into formal documentation
    - Change the icon to something more policy-related (perhaps a clipboard or document icon)
    - Set isActive to true, and comingSoon to false
    - Add a navigation path to "/app/policy-generator"
  2. Backend Processing
    - Utilize the existing transcription workflow with Groq's whisper STT
    - Create a specialized prompt template for the policy generation
    - Configure the LLM to process the transcribed content through the specialized prompt
  3. Frontend Experience
    - Maintain the same three-step process (record, transcribe, generate)
    - Add specialized instructions for policy dictation
    - Update the UI to reflect policy-specific terminology
    - Present the final document in a format that resembles formal policy documentation

  Implementation Process

  1. Make a copy of the TranscriptionPage component
  2. Modify the UI text and instructions to focus on policy generation
  3. Integrate the specialized prompt for the LLM
  4. Update the dashboard card to link to the new feature
  5. Test the end-to-end workflow

  AI Prompt for Coding Implementation

  I need to create a new feature card for a "Policy & Procedure Generator" to replace the "Podcast Summaries" card in our ThinkStream application.
   This feature will help healthcare professionals convert spoken ideas into structured policy documents.

  Please implement the following:

  1. Update the Dashboard:
     - In DashboardPage.tsx, replace the "Podcast Summaries" feature card with "Policy & Procedure Generator"
     - Use this description: "Transform spoken policy concepts into structured, compliant healthcare policy documents following industry
  standards."
     - Change the icon to a document or clipboard icon
     - Set isActive to true and comingSoon to false
     - Add a path to "/app/policy-generator"

  2. Create the Policy Generator Page:
     - Create a new PolicyGeneratorPage.tsx by copying the existing TranscriptionPage.tsx structure
     - Modify the UI to focus on policy generation rather than general transcription
     - Update step descriptions to guide users in dictating policy concepts
     - Keep the same three-step workflow (record, transcribe, generate)

  3. Update the Router:
     - Add the new policy generator route in App.tsx

  4. Integrate the Specialized Prompt:
     - When sending the transcript to the LLM for processing, use this specialized healthcare policy prompt:

  ```json
  {
    "expert_identity": "You are a healthcare management consultant with extensive experience in developing policies and procedures for medical
  offices, particularly in family medicine settings. Your expertise lies in creating structured, concise, and thorough guidelines that ensure
  efficient and compliant operations. You have a deep understanding of healthcare laws, regulations, and best-practice guidelines, which allows
  you to align policies with industry standards. You are skilled at engaging with stakeholders, including nursing staff and healthcare
  professionals, to ensure their input and buy-in. Your approach emphasizes clarity and structure, providing step-by-step instructions that
  eliminate ambiguity. You are adept at designing documentation and communication protocols that facilitate effective record-keeping and
  reporting. You also focus on accountability, identifying responsible parties and compliance monitoring strategies. Your experience in training
  and implementation ensures that staff are well-prepared to adopt new policies. Finally, you incorporate evaluation and continuous improvement
  processes to keep policies relevant and effective. Your comprehensive approach ensures that the policies you develop are easy-to-understand,
  actionable, practical, and fully compliant with healthcare industry standards.",
    "best_prompt": "\nYou are tasked with developing a comprehensive set of policies and procedures specifically for nursing staff at a family
  medicine office. Your objective is to create structured, concise, and thorough guidelines that enhance operational efficiency, ensure compliance
   with healthcare regulations, and improve patient care. \n\nYour response should include the following key elements, clearly organized into
  steps:\n\n1. **Identification and Definition**  \n   - Clearly define the policy objectives, scope, and specific issues being addressed,
  ensuring relevance to the family medicine office setting.\n\n2. **Stakeholder Involvement**  \n   - Describe how nursing staff and other
  relevant healthcare professionals should be involved in the policy development process, ensuring their insights and expertise are
  incorporated.\n\n3. **Compliance and Alignment**  \n   - Ensure the policies align with applicable healthcare laws, regulations, and
  best-practice guidelines, emphasizing the importance of legal and ethical compliance.\n\n4. **Clarity and Structure**  \n   - Provide clear,
  step-by-step instructions that eliminate ambiguity and are easy for staff to follow, ensuring practical usability.\n\n5. **Documentation and
  Communication**  \n   - Outline procedures for documentation, record-keeping, reporting, and communication channels, ensuring transparency and
  accountability.\n\n6. **Accountability and Enforcement**  \n   - Identify responsible parties and explain strategies for monitoring compliance
  and enforcing policies, ensuring accountability.\n\n7. **Training and Implementation**  \n   - Describe how staff training, acknowledgment, and
  implementation should occur to ensure effective adoption and understanding.\n\n8. **Evaluation and Continuous Improvement**  \n   - Include
  timelines for regular review, evaluation methods, feedback mechanisms, and policy updates to ensure continuous improvement and
  relevance.\n\nEnsure the policies are practical, actionable, and fully compliant with healthcare industry standards. Use evidence-based
  practices and logical reasoning to support your response, and consider the diverse scenarios that may arise in a family medicine office.\n\n###
  Expert Role: You are an expert Policy and Procedure Specialist for a medical office. You have extensive knowledge of healthcare regulations,
  nursing operations, compliance standards, and best practices in medical administration. You excel at drafting clear, precise, and actionable
  policy and procedure documents that nursing staff can easily understand and implement effectively. Use deep, detailed reasoning and break the
  problem into smaller parts, employing logical stepwise thinking."
  }

  5. Modify the UI Text:
    - Change title from "Document Creation" to "Policy & Procedure Generator"
    - Replace "Transcript" with "Policy Concept Transcript"
    - Replace "Generated Document" with "Formalized Policy Document"
    - Change the final instruction text to guide users to dictate policy concepts
  6. Update the Output Formatting:
    - Format the generated content to resemble a formal policy document with clear sections
    - Ensure each policy component (Identification, Stakeholder Involvement, etc.) is clearly separated
    - Make sure the document can be easily saved and emailed

  The goal is to leverage our existing transcription and generation infrastructure while creating a specialized tool for healthcare policy
  generation. The user experience should be familiar to users of our transcription feature but tailored specifically for policy creation.

  This implementation will provide a valuable tool for healthcare administrators to quickly create properly structured, compliant policies from
  spoken concepts, saving them significant time and ensuring consistency in policy documentation.