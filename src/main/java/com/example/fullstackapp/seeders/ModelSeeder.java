package com.example.fullstackapp.seeders;

import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import com.example.fullstackapp.model.AIModel;
import com.example.fullstackapp.repository.ModelRepository;
import com.example.fullstackapp.service.APIKeyService;




@Component
public class ModelSeeder implements CommandLineRunner{
    
    private final ModelRepository modelRepository;

    private final APIKeyService apiKeyService;

    public ModelSeeder(ModelRepository modelRepository, APIKeyService apiKeyService) {
        this.modelRepository = modelRepository;
        this.apiKeyService = apiKeyService;
    }

    @Override
    public void run(String... args) throws Exception{
        if (modelRepository.count() == 0)
        {
            AIModel gemini = new AIModel(null, "Gemini-1.5-Flash-8B", "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent", "Google", apiKeyService.getAPIKey("Google"), "");
            AIModel mistral = new AIModel(null, "mistral-large-latest", "https://api.mistral.ai/v1/chat/completions", "Mistral", apiKeyService.getAPIKey("mistral"), "");
            AIModel llama = new AIModel(null, "llama-3.1-8b-instant", "https://api.groq.com/openai/v1/chat/completions", "Groq", apiKeyService.getAPIKey("groq"), "");
            modelRepository.save(gemini);
            modelRepository.save(mistral);
            modelRepository.save(llama);

            System.out.println("Seeding completed");
        }
    }
}
