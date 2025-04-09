// frontend/src/App.jsx
import React, { useState } from "react";
import PdfUpload from "./components/PdfUpload";
import ChatSection from "./components/ChatSection";
``;

function App() {
  const [activeTab, setActiveTab] = useState("upload"); // "upload" | "chat"

  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <header className="relative bg-white px-6 py-4 shadow-md flex items-center justify-between border-b">
        {/* Left: Company Logo */}
        <div className="w-20 h-10 flex items-center">
          <img
            src="../../enova_logo.jpg"
            alt="Company Logo"
            className="h-full object-contain"
          />
        </div>

        {/* Center: Title */}
        <h1 className="absolute left-1/2 transform -translate-x-1/2 text-2xl font-bold text-red-600">
          AI Musaed مساعد
        </h1>

        {/* Right: User Email */}
        <div className="text-sm text-gray-600">Omar_ali@enova-me.com</div>
      </header>

      {/* Action Buttons */}
      <div className="flex justify-center space-x-4 bg-white py-4 shadow-sm border-b">
        <button
          onClick={() => setActiveTab("upload")}
          className={`px-4 py-2 rounded font-semibold ${
            activeTab === "upload"
              ? "bg-blue-600 text-white"
              : "bg-gray-200 text-gray-800 hover:bg-gray-300"
          }`}
        >
          📄 Upload PDF
        </button>
        <button
          onClick={() => setActiveTab("chat")}
          className={`px-4 py-2 rounded font-semibold ${
            activeTab === "chat"
              ? "bg-blue-600 text-white"
              : "bg-gray-200 text-gray-800 hover:bg-gray-300"
          }`}
        >
          💬 Chat with Gemini
        </button>
      </div>

      {/* Main Layout: Sidebar + Main Chat Area */}
      <div className="flex flex-1">
        {/* Sidebar Placeholder (History & logo etc.) */}
        <aside className="w-[250px] bg-white border-r hidden md:block p-4 text-gray-500 shadow-sm">
          {/* Add sidebar content later */}
          <div className="text-lg font-semibold mb-4">🕓 History</div>
          <div className="text-sm text-gray-400">Coming soon...</div>
        </aside>

        {/* Main Area */}
        <main className="flex-1 flex p-0 overflow-hidden bg-gray-100">
          {activeTab === "upload" && <PdfUpload />}
          {activeTab === "chat" && <ChatSection />}
        </main>
      </div>
    </div>
  );
}

export default App;
