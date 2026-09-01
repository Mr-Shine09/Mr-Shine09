<div align="center">

<img src="assets/profile-header.svg" width="100%" alt="Oak Soe Khant — Computer Engineering, De Anza CC. Seeking internships.">

<p align="center">
  <a href="#" title="Portfolio (coming soon)"><img src="https://api.iconify.design/mdi/web.svg?color=%2338BDF8" width="28" height="28" alt="Portfolio"></a>&nbsp;&nbsp;&nbsp;
  <a href="https://www.linkedin.com/in/oak-soe-khant-350252362" title="LinkedIn"><img src="https://api.iconify.design/simple-icons/linkedin.svg?color=%230A66C2" width="28" height="28" alt="LinkedIn"></a>&nbsp;&nbsp;&nbsp;
  <a href="https://devpost.com/oaksoekhant182209" title="Devpost"><img src="https://api.iconify.design/simple-icons/devpost.svg?color=%23003E54" width="28" height="28" alt="Devpost"></a>&nbsp;&nbsp;&nbsp;
  <a href="https://leetcode.com/u/OakS0eKhant/" title="LeetCode"><img src="https://api.iconify.design/simple-icons/leetcode.svg?color=%23FFA116" width="28" height="28" alt="LeetCode"></a>&nbsp;&nbsp;&nbsp;
  <a href="https://github.com/Mr-Shine09/Mr-Shine09/raw/main/Oak_Soe_Khant_Resume.pdf" title="Résumé"><img src="https://api.iconify.design/mdi/file-pdf-box.svg?color=%23EC1C24" width="28" height="28" alt="Résumé"></a>&nbsp;&nbsp;&nbsp;
  <a href="mailto:oaksoekhant255@gmail.com" title="Email"><img src="https://api.iconify.design/simple-icons/gmail.svg?color=%23EA4335" width="28" height="28" alt="Email"></a>
</p>

**4.0 GPA** · Honors Student · CIS Tutoring Assistant · VP, Competitive Programming Club

</div>

---

<p align="center">
🤖&nbsp;&nbsp;AI technology fanatic, passionate about building assistive technologies and productivity-boosting tools.&nbsp;&nbsp;🦾
</p>

---

## Hardware

### 01 / [VisionAssist](https://github.com/Mr-Shine09/VisionAssist)

**The problem:** Navigation aids for blind users assume a phone, a data plan, and a cloud
endpoint. All three fail exactly when someone is outdoors and alone.

**The solution:** A head-mounted device that identifies obstacles and speaks them aloud —
*"stop, chair, 2 steps ahead"* — entirely on-device. YOLOv8n runs at ~5 FPS on a Raspberry Pi 5
with an Arducam IMX708, and audio goes out over Bluetooth earbuds. No phone, no cloud, no
internet. Built over six weeks by a five-person team at De Anza as an Infineon-sponsored
capstone and demoed to their engineers.

I evaluated Infineon's XENSIV 60 GHz radar for depth, determined it would not ship inside the
project window, and designed the monocular bounding-box distance estimator that replaced it —
which is what carried the final demo.

<p>
  <strong>Stack</strong>&nbsp;&nbsp;
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg" height="26" alt="Python" title="Python">&nbsp;
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/pytorch/pytorch-original.svg" height="26" alt="PyTorch" title="PyTorch (YOLOv8n)">&nbsp;
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/opencv/opencv-original.svg" height="26" alt="OpenCV" title="OpenCV">&nbsp;
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/flask/flask-original.svg" height="26" alt="Flask" title="Flask">&nbsp;
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/raspberrypi/raspberrypi-original.svg" height="26" alt="Raspberry Pi" title="Raspberry Pi 5">
</p>

---

## Software

### 02 / [PokeDesk](https://github.com/Mr-Shine09/PokeDesk)

**The problem:** When a coding agent is working, you either sit and watch a terminal or you walk
away and lose track of whether it finished, stalled, or failed.

**The solution:** A pixel mascot that lives at the bottom edge of your Mac and shows agent state
at a glance — it sits down and types while Claude Code or Codex works, fist-pumps on success,
goes dizzy on failure, and curls up to sleep after 23:00. A native AppKit menu-bar accessory
that never activates over your work and **never reads a single character** of your prompts,
code, or terminal output; it reads hook events only. I measured the idle-CPU budget rather than
guessing at it, and published the failed measurement alongside the passing one.

<p>
  <strong>Stack</strong>&nbsp;&nbsp;
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/swift/swift-original.svg" height="26" alt="Swift" title="Swift">&nbsp;
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/apple/apple-original.svg" height="26" alt="macOS AppKit" title="macOS / AppKit">&nbsp;
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/xcode/xcode-original.svg" height="26" alt="Xcode" title="Xcode">&nbsp;
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg" height="26" alt="Python" title="Python (sprite tooling)">
</p>

---

### 03 / [Zephyr](https://github.com/Mr-Shine09/Zephyr)

**The problem:** You give an agent a real job — a migration, a refactor, a test suite to green —
and then you are chained to the keyboard for forty minutes in case it stops to ask you something.

**The solution:** Zephyr streams a live Mistral Vibe session to your phone and lets you answer
it from there. It adds `pre_agent` and `agent_waiting` observer hooks so a desktop companion can
tell the difference between *working* and *blocked on you*, then hands you the approval prompt
wherever you are. macOS mascot plus an iOS companion app, sharing one event bridge. Built for
the Mistral Vibe Hackathon, Track 02.

<p>
  <strong>Stack</strong>&nbsp;&nbsp;
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg" height="26" alt="Python" title="Python">&nbsp;
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/swift/swift-original.svg" height="26" alt="Swift" title="Swift (iOS + macOS)">&nbsp;
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/nixos/nixos-original.svg" height="26" alt="Nix" title="Nix flake">&nbsp;
  <img src="https://api.iconify.design/simple-icons/mistralai.svg?color=%23FA520F" height="26" alt="Mistral" title="Mistral Vibe CLI">
</p>

---

### 04 / [Look-Out](https://github.com/Mr-Shine09/Look-Out)

**The problem:** Every alert tool ever built — Google Alerts, RSS, saved searches — is designed
to notify you *more*. They re-fire on every duplicate and every reword, so you mute them, and
then you miss the one that mattered.

**The solution:** Look-Out is a suppression engine. Before anything reaches you it asks two
questions: *have I effectively shown you this already?* (semantic dedup against alert history in
Redis vector search) and *does this actually matter to you?* (an LLM judging against a spec
compiled from your plain-English ask). Only items clearing both bars surface. The longer it
runs, the quieter it gets. On a match it runs a five-stage pipeline — Scout → Fit Judge →
Strategist → Drafter → Critic — to draft a response for your approval, and your thumbs up/down
retrains the relevance threshold live, so the ranking visibly re-sorts during a session.

Built at the UC Berkeley AI Hackathon 2026. **Lead author — 27 of the 52 commits**, across a
five-person team; I built the judge, the dedup memory, and the agent pipeline.

<p>
  <strong>Stack</strong>&nbsp;&nbsp;
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg" height="26" alt="Python" title="Python">&nbsp;
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/javascript/javascript-original.svg" height="26" alt="JavaScript" title="JavaScript">&nbsp;
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/redis/redis-original.svg" height="26" alt="Redis" title="Redis vector search">&nbsp;
  <img src="https://api.iconify.design/simple-icons/anthropic.svg?color=%23D97757" height="26" alt="Claude API" title="Claude API">&nbsp;
  <img src="https://api.iconify.design/simple-icons/ollama.svg?color=%23888888" height="26" alt="Ollama" title="Ollama (local judge)">
</p>

---

### 05 / [Huffman Encoding Algorithm](https://github.com/Mr-Shine09/Huffman-Encoding-Algorithm) · [Live demo](https://mr-shine09.github.io/Huffman-Encoding-Algorithm/)

**The problem:** Huffman coding is taught as a diagram on a whiteboard, which hides the fact
that it is really three different data structures handing work to each other.

**The solution:** A full C++ implementation where each stage owns exactly one structure — a
direct-address **hash table** counts frequencies in O(1), a **sorted linked list** keeps leaves
ordered by frequency, and a **binary tree** merges them greedily into prefix-free codes.
Composition and pointers throughout, no inheritance. The browser demo builds the frequency
table, tree, codes, and live compression ratio as you type. CIS 22C Honors project.

<p>
  <strong>Stack</strong>&nbsp;&nbsp;
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/cplusplus/cplusplus-original.svg" height="26" alt="C++" title="C++17">&nbsp;
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/javascript/javascript-original.svg" height="26" alt="JavaScript" title="JavaScript (demo)">&nbsp;
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/cmake/cmake-original.svg" height="26" alt="Build" title="g++ / Clang">
</p>

---

## Also working with

<p>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/java/java-original.svg" height="26" alt="Java" title="Java">&nbsp;
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/typescript/typescript-original.svg" height="26" alt="TypeScript" title="TypeScript">&nbsp;
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/fastapi/fastapi-original.svg" height="26" alt="FastAPI" title="FastAPI">&nbsp;
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/numpy/numpy-original.svg" height="26" alt="NumPy" title="NumPy">&nbsp;
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/pandas/pandas-original.svg" height="26" alt="pandas" title="pandas">&nbsp;
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/scikitlearn/scikitlearn-original.svg" height="26" alt="scikit-learn" title="scikit-learn">&nbsp;
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/supabase/supabase-original.svg" height="26" alt="Supabase" title="Supabase">&nbsp;
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/git/git-original.svg" height="26" alt="Git" title="Git">&nbsp;
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/linux/linux-original.svg" height="26" alt="Linux" title="Linux">
</p>
