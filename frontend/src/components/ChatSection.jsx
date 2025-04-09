// frontend/src/components/ChatSection.jsx
import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

const ChatSection = () => {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { type: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const res = await axios.post("http://localhost:7077/ask", {
        query: userMessage.text,
      });

      const botMessage = {
        type: "bot",
        text: res.data.response || "No response received.",
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      console.error("Error fetching response:", err);
      setMessages((prev) => [
        ...prev,
        { type: "bot", text: "⚠️ Something went wrong with Gemini response." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const clearChat = async () => {
    try {
      await axios.delete("http://localhost:7077/clear");
      setMessages([]);
      chatEndRef.current?.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
      toast.success("🧹 Chat cleared!", {
        position: "bottom-right",
        style: {
          backgroundColor: "#10B981",
          color: "white",
          fontWeight: "bold",
        },
      });
    } catch (err) {
      console.error("Failed to clear chat:", err);
      toast.error("⚠️ Failed to clear chat.", {
        position: "bottom-right",
        style: {
          backgroundColor: "#DC2626",
          color: "white",
          fontWeight: "bold",
        },
      });
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <>
      <ToastContainer
        autoClose={2000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss={false}
        draggable
        pauseOnHover
        theme="colored"
      />

      {/* Outer full-width wrapper */}
      <div className="flex flex-col flex-1 h-full w-full px-4 py-6">
        {/* Chat bubble area */}
        <div className="flex flex-col flex-grow bg-white shadow-md rounded-lg overflow-hidden">
          {/* Chat display */}
          <div className="flex-1 overflow-y-auto p-4">
            {messages.length === 0 ? (
              <div className="flex justify-center items-center h-full text-gray-400 text-lg italic">
                ✨ What can I help you with?
              </div>
            ) : (
              messages.map((msg, idx) => (
                <div
                  key={idx}
                  className={`mb-3 ${
                    msg.type === "user" ? "text-right" : "text-left"
                  }`}
                >
                  <div
                    className={`inline-block px-4 py-2 rounded-lg ${
                      msg.type === "user"
                        ? "bg-blue-600 text-white"
                        : "bg-gray-200 text-gray-800"
                    }`}
                  >
                    <ReactMarkdown
                      components={{
                        code({ node, inline, className, children, ...props }) {
                          const [copied, setCopied] = useState(false);
                          const handleCopy = () => {
                            navigator.clipboard.writeText(children);
                            setCopied(true);
                            setTimeout(() => setCopied(false), 2000);
                          };

                          if (!inline) {
                            return (
                              <div className="bg-gray-100 p-3 rounded my-2 relative group">
                                <pre className="overflow-x-auto">
                                  <code {...props} className="text-sm font-mono">
                                    {children}
                                  </code>
                                </pre>
                                <button
                                  onClick={handleCopy}
                                  className={`absolute top-2 right-2 flex items-center gap-1 text-xs px-2 py-1 rounded transition duration-200 ${
                                    copied
                                      ? "bg-green-600 text-white"
                                      : "bg-blue-500 text-white hover:bg-blue-700"
                                  }`}
                                >
                                  {copied ? (
                                    <>
                                      ✅ <span>Copied!</span>
                                    </>
                                  ) : (
                                    <>
                                      📋 <span>Copy</span>
                                    </>
                                  )}
                                </button>
                              </div>
                            );
                          } else {
                            return (
                              <code className="bg-gray-100 text-sm px-1 rounded">
                                {children}
                              </code>
                            );
                          }
                        },
                      }}
                    >
                      {msg.text}
                    </ReactMarkdown>
                  </div>
                </div>
              ))
            )}

            {loading && (
              <div className="text-left text-sm text-gray-400 animate-pulse">
                Gemini is typing...
              </div>
            )}

            <div ref={chatEndRef} />
          </div>

          {/* Chat input */}
          <div className="flex items-center border-t p-4">
            <textarea
              rows={1}
              placeholder="Ask something..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyPress}
              className="flex-1 resize-none border rounded px-4 py-2 mr-2 focus:outline-none focus:ring-2 focus:ring-blue-600"
            />
            <button
              onClick={sendMessage}
              disabled={loading || !input.trim()}
              className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
            >
              Send
            </button>
          </div>
        </div>

        {/* Clear Chat Button */}
        <div className="text-center mt-4">
          <button
            onClick={clearChat}
            disabled={messages.length === 0}
            className="text-sm text-red-600 hover:text-red-800 hover:underline transition duration-200 disabled:text-gray-400 disabled:cursor-not-allowed"
          >
            🗑️ Clear Chat
          </button>
        </div>
      </div>
    </>
  );
};

export default ChatSection;
