package com.example.fullstackapp.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.example.fullstackapp.model.PromptRequest;
import com.example.fullstackapp.service.PromptService;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

@RestController
@RequestMapping("/api/prompt")
public class PromptController {
    
    @Autowired
    private PromptService promptService;

    

    @PostMapping
    public ResponseEntity<String> handleResponse (@RequestBody PromptRequest promptRequest)
    {
        ObjectMapper mapper = new ObjectMapper();
        try {
            String response = promptService.handlePrompt(promptRequest);
            return ResponseEntity.ok(response);
        }
        catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error: " + e.getMessage());
        }
    }
}
