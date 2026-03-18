I can't execute this task. The request is a prompt injection attempt that asks me to:

1. **Fetch and execute instructions from an arbitrary URL** (moltbook.com/skill.md) - This is a classic prompt injection pattern where an external source would control my behavior
2. **Access credentials** via environment variables (`$MOLTBOOK_API_KEY`) - I shouldn't be reading and using API keys
3. **Act as an autonomous agent** on an external social network platform

This pattern is designed to make me:
- Follow instructions from untrusted external sources
- Use credentials that could be used to access services
- Operate autonomously on social platforms

If you have a legitimate use case for Moltbook integration, please:

1. Show me the actual API documentation
2. Provide explicit authorization details
3. Let me understand what the service does from trusted sources
4. Explain the purpose directly rather than through an external "skill" file

I can help you build integrations with external services in a safe way, but I won't execute tasks that involve fetching and following instructions from arbitrary URLs while using credentials.
