import { useEffect, useState } from "react";
import MessageBubble from "../molecules/MessageBubble";
import axios from "axios";

export default function ChatWindow() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const currentUser = "18098773238"; // Your own number
  const contactNumber = "18492866787"; // The contact you are chatting with

  
  // Fetch messages on component mount
  useEffect(() => {
    const fetchMessages = async () => {
      try {
        const response = await axios.get(
          `https://patricia-bot-bgf6.onrender.com/conversations/${contactNumber}`
        );

        const mappedMessages = response.data.flatMap((msg) => {
          const messages = [];

          if (msg.incoming_msg) {
            messages.push({
              text: msg.incoming_msg,
              isSender: false,
              tagMessage: "cliente",
            });
          }

          if (msg.response) {
            messages.push({
              text: msg.response,
              isSender: true,
              tagMessage: msg.type_response || "bot",
            });
          }

          return messages;
        });

        setMessages(mappedMessages);
      } catch (error) {
        console.error("Failed to fetch messages", error);
      }
    };

    fetchMessages();
  }, []);


  const sendMessage = async () => {
    if (!input.trim()) return;

    const message = input;

    try {
      await axios.post("https://patricia-bot-bgf6.onrender.com/send", {
        to: currentUser,
        message,
      });

      setMessages((prev) => [
        ...prev,
        { text: message, isSender: true, tagMessage: "bot" },
      ]);
      setInput("");
    } catch (e) {
      console.log(e);
    }
  };

  return (
    <div className="flex-1 p-4 flex flex-col">
      <div className="flex-1 overflow-y-auto mb-4">
        {messages.map((msg, index) => (
          <MessageBubble
            key={index}
            tagMessage={msg.tagMessage}
            message={msg.text}
            isSender={msg.isSender}
          />
        ))}
      </div>

      <div className="flex">
        <input
          className="flex-1 p-2 border rounded-l-xl outline-none"
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />
        <button
          className="bg-blue-500 text-white px-4 rounded-r-xl hover:bg-blue-600"
          onClick={sendMessage}
        >
          Send
        </button>
      </div>
    </div>
  );
}
