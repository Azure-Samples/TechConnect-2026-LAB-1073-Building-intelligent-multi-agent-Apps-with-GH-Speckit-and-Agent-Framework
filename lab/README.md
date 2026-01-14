
# HelloWeather — Spec‑Driven Multi‑Agent Web Application

HelloWeather is a **hands‑on lab project** demonstrating how to build a **spec‑driven, multi‑agent, concurrent workflow** using:

- GitHub **Spec Kit**
- **Microsoft Agent Framework**
- **Azure OpenAI**
- **FastAPI** for the web UI
- **VS Code** for development

## 🎯 What You Will Build

A simple web app that:

1. Asks the user for a **one‑sentence introduction** and a **city**.
2. Triggers two agents **concurrently**:
   - **WeatherAgent** → Produces a short approximate weather tip.
   - **CityAgent** → Produces a short city‑specific guidance sentence.
3. Aggregates both results into **one friendly, under‑60‑word message**.
4. Streams live updates to the web UI.

## 🧩 Why This Lab

This lab teaches:

- Multi‑agent orchestration (fan‑out / fan‑in)
- Spec‑driven development workflows using Spec Kit
- Concurrent execution using Microsoft Agent Framework
- Clean separation into Constitution → Specification → Plan → Tasks → Implementation
- How to build a functional AI prototype **without any static data**

## 📚 Structure of This Repository

This repository contains the following learning modules:

1. **01‑prerequisites** — Environment setup, dependencies, Spec Kit installation  
2. **02‑constitution** — High‑level purpose, principles, agent definitions  
3. **03‑specification** — What/Why of the app, constraints, user journey  
4. **04‑plan** — File layout, orchestration design, frontend plan  
5. **05‑tasks** — Step‑by‑step actionable task list  
6. **06‑implementation** — Final code generation using Spec Kit  
7. **07‑WorkingCode** — Working Code  

Each module includes ready‑to‑copy prompts for GitHub Copilot + Spec Kit.

## 🚀 Outcomes

By the end of this lab, you will have:

- A working **multi‑agent FastAPI application**
- Fully generated Python code (agents, orchestrator, UI)
- A reproducible workflow for building Spec‑driven AI applications
- A GitHub‑ready project structure

## 🔧 Requirements

- Python 3.10+
- Azure CLI
- Azure OpenAI resource
- Spec Kit installed via UVX

Lets get started - Proceed to [01-Prerequisites](../lab/01-prerequisites/README.md) once these prerequisites are met.
