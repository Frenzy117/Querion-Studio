import React, { useEffect, useState } from 'react'
import Markdown from 'react-markdown';
import Select from '@mui/material/Select';
import { IconButton, Button, FormControl, InputLabel, MenuItem } from '@mui/material';
import {Alert, AlertTitle} from '@mui/material';
import { Panel, PanelGroup, PanelResizeHandle } from 'react-resizable-panels';
import { GoChevronRight } from "react-icons/go";
import { TextareaAutosize } from '@mui/material';
import { Link } from 'react-router-dom';

const Playground = () => {
  const [models, setModels] = useState([]);
  const [chosenModel, setChosenModel] = useState("");
  const [prompt, setPrompt] = useState("");
  const [systemInstruction, setSystemInstruction] = useState("");
  const [context, setContext] = useState("");
  const [recentPrompts, setRecentPrompts] = useState([
    "How to implement a chat application with React?",
    "Create a tutorial for building a REST API with Node.js",
    "Compare SQL and NoSQL databases",
    "Explain quantum computing like I'm 10",
    "Write a story about space exploration",
  ]);
  const [listedPrompt, setListedPrompt] = useState("");
  const [response, setResponse] = useState("");
  const [templates, setTemplates] = useState({
    "Story Writer": "Write a story about {topic} with {emotion} tone.",
    "Simple Explainer": "Explain {concept} to me like I'm {age} years old.",
    "Tutorial Creator": "Create a step-by-step tutorial for {task}.",
    "Comparison": "Compare and contrast {item1} and {item2}.",
    "Brainstorming": "Brainstorm 5 creative ideas about {topic}.",
    "Summarizer": "Summarize this text: {text}",
  });
  const [template, setTemplate] = useState("");

  useEffect(() => {
    fetch("http://localhost:8080/api/models").then((response) => {
      return response.json();
    }).then((data) => {
      const modelNames = data.map(element => element.name);
      setModels(modelNames);
    })
    .catch((e) => {
      console.log(e);
    });
  }, []);

  const handleChange = (e) => {
    const value = e.target.value;
    setChosenModel(value);
  };
  const handlePromptChange = (e) => {
    setPrompt(e.target.value);
  };
  const handleInstructionChange = (e) => setSystemInstruction(e.target.value);
  const handleContextChange = (e) => setContext(e.target.value);
  const handleTemplateChange = (e) => {
    const value = e.target.value;
    setTemplate(value);
  };

  const handleSubmit = async () => {
    const request = {
      modelName: chosenModel,
      systemInstruction: systemInstruction,
      conversationalContext: context,
      prompt: prompt
    };
    
    try {
      const res = await fetch("http://localhost:8080/api/prompt", {
        method: "POST",
        headers: {
          'Access-Control-Allow-Origin': 'http://localhost:3000',
          "Content-Type": "application/json",
        },
        body: JSON.stringify(request)
      });
      const data = await res.text();
      setResponse(data);
      console.log(response);
    } catch (e) {
      console.log("Prompt request failed:", e);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault(); // prevent newline
      handlePromptChange(e);
    }
  };

  return (
    <div className="bg-[#121212] h-screen max-h-screen">
      <div className="text-[#F8F8F8] px-6 py-2 flex justify-between items-center relative">
        <div className="text-3xl font-extralight text-[#3ABEFF] font-sans">
          <Link to={'/home'}>
            Qrion
          </Link>
        </div>
        <div className="flex gap-5">
          <Button sx={{ color: "#F8F8F8", textTransform: "none", fontFamily: "satoshi" }} variant='text'>History</Button>
          <Button sx={{ color: "#F8F8F8", textTransform: "none", fontFamily: "satoshi" }} variant='text'>Settings</Button>
          <Button sx={{ color: "#F8F8F8", textTransform: "none", fontFamily: "satoshi" }} variant='text'>Logout</Button>
        </div>
      </div>
      <PanelGroup direction='horizontal' className="bg-[#121212] text-gray-900 flex h-screen overflow-auto">
        <Panel className="h-screen flex flex-col bg-[#1A1A1A] m-2 rounded-xl p-1">
          <div className='overflow-y-auto flex-column h-full justify-between'>
            <div className="relative m-2 flex rounded-xl w-full flex-row justify-center">
              <FormControl sx={{ width: "33.33%" }}>
                <InputLabel id="model-select-label" className="block text-white text-sm font-medium mb-2" sx={{ fontFamily: 'satoshi', color: "#F8F8F8" }}>
                  Choose Your Model
                </InputLabel>
                <Select  value={chosenModel} onChange={handleChange} labelId="model-select-label" label="Choose Your Model" sx={{ borderRadius: "0.75em", color: "#F8F8F8", backgroundColor: "#202020", fontFamily: "satoshi" }}>
                  {models.map((model, index) => {
                    return <MenuItem key={index} value={model} dense={true} sx={{ paddingTop: "0", background: "inherit", fontFamily: "satoshi" }}>
                      {model}
                    </MenuItem>;
                  })};
                </Select>
              </FormControl>
            </div>
            <div id="messagesContainer" className="bg-[#1A1A1A] flex-1 overflow-y-auto h-fit text-[#F8F8F8] rounded-2xl p-4 m-3 mb-2 font-sans">
              {response && (
                <Markdown>
                  {response}
                </Markdown>
              )}
            </div>
            <div className="p-2.5 h-fit min-h-12 m-0.5 outline-none justify-center items-center align-middle flex bg-[#202020] focus:outline-none focus:ring-0 focus:ring-grey focus:ring-opacity-40 shadow-lg resize-none rounded-3xl">
              <TextareaAutosize
                placeholder='Say something...'
                onChange={handlePromptChange}
                value={prompt}
                maxRows={15}
                style={{ height: "25px" }}
                className='w-full outline-none font-sans bg-inherit backdrop-blur-lg mx-2 placeholder-gray placeholder-opacity- caret-[#3ABEFF] text-white resize-none'
              />
              <div className='flex justify-end align-bottom rounded-full bg-[#3ABEFF]'>
                <IconButton variant='contained' aria-label='send' size='small' color='primary' onClick={handleSubmit}>
                  <GoChevronRight className='w-fit' />
                </IconButton>
              </div>
            </div>
          </div>
        </Panel>
        <PanelResizeHandle />
        <Panel className="h-full flex flex-col bg-[#1A1A1A] rounded-xl p-2 m-2">
          <div className="bg-[#202020] text-white px-5 py-4 font-medium font-sans rounded-xl">Playground</div>
          <div className="flex-1 p-5 overflow-y-auto">
            <div className="bg-[#1A1A1A] rounded-lg py-4 my-2.5">
              <h3 className="text-[#F8F8F8] font-medium my-1.5 text-sm font-sans">Prompt Templates</h3>
              <FormControl fullWidth>
                <InputLabel id="template-select-label" className="block text-sm font-medium mb-2 font-sans" sx={{ color: "#F8F8F8", fontFamily: 'satoshi' }}>
                  Choose Your Template
                </InputLabel>
                <Select value={template} onChange={handleTemplateChange} labelId="template-select-error-label" label="Choose Your Template"
                  sx={{ color: "#F8F8F8", backgroundColor: "#202020", fontFamily: "satoshi" }}>
                  {Object.entries(templates).map(([listedTemplate, index]) => {
                    return <MenuItem key={index} value={listedTemplate} sx={{ fontFamily: "satoshi", color: "#202020" }}>
                      {listedTemplate}
                    </MenuItem>;
                  })};
                </Select>
              </FormControl>
            </div>

            <div className="bg-[#1A1A1A] rounded-lg py-4 my-2.5 ">
              <h3 className="text-[#F8F8F8] font-medium my-1.5 text-sm font-sans">System Instructions </h3>
                <TextareaAutosize
                  placeholder='Provide instructions to your model here...'
                  onChange={handleInstructionChange}
                  value={systemInstruction}
                  maxRows={15}
                  minRows={5}
                  style={{ height: "25px" }}
                  className='w-full outline-none backdrop-blur-lg p-3 shadow-sm rounded-lg placeholder-gray placeholder-opacity- caret-[#3ABEFF] font-sans text-white bg-[#202020] resize-none'
                />
                {chosenModel.includes('mistral') && (
                  <Alert sx={{backgroundColor: "#1A1A1A", color: "amber"}} className="my-2 border text-[#F8F8F8] font-sans" severity="warning">
                    <AlertTitle className=" font-sans">Warning</AlertTitle>
                    {chosenModel} is not fine-tuned for instruction following. Your system instruction will therefore be prepended to the prompt.
                  </Alert>
                )}
                <div className="flex gap-2 my-1">
                  <button id="sendToChat" className="bg-[#3ABEFF] hover:bg-[#66D6FF] text-[#F8F8F8] px-3 py-2 rounded text-sm font-sans">Send to Chat</button>
                  <button id="clearPrompt" className="bg-[#3ABEFF] hover:bg-[#66D6FF] text-[#F8F8F8] px-3 py-2 rounded text-sm font-sans" onClick={(e) => {setSystemInstruction("")}}>Clear</button>
              </div>
            </div>
              
            <div className="bg-[#1A1A1A] rounded-lg py-4 my-2.5 ">
              <h3 className="text-[#F8F8F8] font-medium my-1.5 text-sm font-sans">Conversation Context</h3>
                <TextareaAutosize
                  placeholder='Set your conversation context here...'
                  onChange={handleContextChange}
                  value={context}
                  maxRows={15}
                  minRows={5}
                  style={{ height: "25px" }}
                  className='w-full outline-none backdrop-blur-lg p-3 rounded-lg placeholder-gray placeholder-opacity- caret-[#3ABEFF] font-sans text-white bg-[#202020] resize-none'
                />
              <div className="flex gap-2 my-1">
              </div>
            </div>

            <div className="bg-[#1A1A1A] rounded-lg py-4 my-2.5 ">
              <h3 className="text-[#F8F8F8] font-medium mb-3 text-sm font-sans">Recent Prompts</h3>
              <div className="bg-[#202020] rounded-lg p-4 shadow-sm">
                <div className="max-h-48 overflow-y-auto">
                  {recentPrompts.map((recentPrompt, index) => {
                    return <option className="history-item py-2 px-2 border-b border-[#3ABEFF] cursor-pointer text-sm text-[#A0A0A0] font-sans hover:bg-[#232323]" onClick={handlePromptChange} value={recentPrompt}>{recentPrompt}</option>
                  })}
                </div>
              </div>
            </div>
          </div>
        </Panel>
      </PanelGroup>
    </div>
  );
}

export default Playground;