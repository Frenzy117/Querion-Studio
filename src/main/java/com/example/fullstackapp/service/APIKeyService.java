package com.example.fullstackapp.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
public class APIKeyService {
    
    @Value("${google.api.key}")
    private String googleKey;

    @Value("${mistral.api.key}")
    private String mistralKey;

    @Value("${groq.api.key}")
    private String groqKey;

    public String getAPIKey(String model)
    {
        return switch (model.toLowerCase())
        {
            case "google" -> googleKey;
            case "mistral" -> mistralKey;
            case "groq" -> groqKey;
            default -> throw new RuntimeException("API Key not found for the model: " + model);
        };
    }
}
