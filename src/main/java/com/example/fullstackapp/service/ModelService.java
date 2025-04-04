package com.example.fullstackapp.service;

import com.example.fullstackapp.model.AIModel;
import com.example.fullstackapp.model.User;
import com.example.fullstackapp.repository.ModelRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class ModelService {
    @Autowired
    private ModelRepository modelRepository;

    public List<AIModel> getAllAiModels() {
        return modelRepository.findAll();
    }

    public Optional<AIModel> getModelById(Long id) {
        return modelRepository.findById(id);
    }

    public AIModel getModelByName(String name) {
        return modelRepository.findByName(name).orElseThrow(() -> new RuntimeException("Model not found."));
    }

    public AIModel createModel(AIModel model)
    {
        return modelRepository.save(model);
    }

    public AIModel updateModel(Long id, AIModel modelDetails)
    {
        AIModel model = modelRepository.findById(id).orElseThrow(()-> new RuntimeException("User not found."));
        model.setName(modelDetails.getName());
        model.setAuthKey(modelDetails.getAuthKey());
        return modelRepository.save(model);
    }
    
    public void deleteModel(Long id)
    {
        modelRepository.deleteById(id);
    }
}
