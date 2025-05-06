"use client"

import { useEffect, useRef, useState } from "react";
import axios from "axios";
import MessageBubble from "./MessageBubble";

type ChatWindowProps = {
    currentUser: string;
};

type MessagesReceived = {
    incoming_msg: string;
    response: string;
    type_response: 'bot' | 'gpt' | 'seller' | 'client';
};

type Message = {
    tagMessage: 'bot' | 'gpt' | 'seller' | 'client';
    message: string;
    isSender: boolean;
};

export default function ChatWindow({ currentUser }: ChatWindowProps) {
    const API_BASE_PROTOCOLE = process.env.NEXT_PUBLIC_API_PROTOCOLE;
    const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState("");
    const scrollRef = useRef<HTMLDivElement | null>(null);

    useEffect(() => {
        const fetchMessages = async () => {
            try {
                const response = await axios.get(
                    `${API_BASE_PROTOCOLE}${API_BASE_URL}/conversations/${currentUser}`
                );

                const mappedMessages = response.data.flatMap((msg: MessagesReceived) => {
                    const messagesObj = [];
                    if (msg.incoming_msg) {
                        messagesObj.push({
                            message: msg.incoming_msg,
                            isSender: false,
                            tagMessage: "client",
                        });
                    }

                    if (msg.response) {
                        messagesObj.push({
                            message: msg.response,
                            isSender: true,
                            tagMessage: msg.type_response || "bot",
                        });
                    }
                    return messagesObj;
                });
                setMessages(mappedMessages);

                const ws = new WebSocket(`wss://${API_BASE_URL}/ws`)
                ws.onmessage = (event) => {
                    const messagesObj2: Message[] = [];
                    const data = JSON.parse(event.data);
                    debugger
                    if (data.type === "message") {
                        const payload = data.payload
                        if (payload.incoming_msg) {
                            messagesObj2.push({
                                message: payload.incoming_msg,
                                isSender: false,
                                tagMessage: "client",
                            });
                        }
                        if (payload.response) {
                            messagesObj2.push({
                                message: payload.response,
                                isSender: true,
                                tagMessage: payload.type_response || "bot",
                            });
                        }
                        setMessages((prevMessages) => [...prevMessages, ...messagesObj2]);
                    }
                }
            } catch (error) {
                console.error("Failed to fetch messages", error);
            }
        };
        fetchMessages();
    }, []);

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [messages]);

    const sendMessage = async () => {
        if (!input.trim()) return;

        const message = input;

        try {
            debugger
            await axios.post(`${API_BASE_PROTOCOLE}${API_BASE_URL}/send`, {
                to: currentUser,
                message,
            });

            setMessages((prev: Message[]) => [
                ...prev,
                {
                    message: message,
                    isSender: true,
                    tagMessage: "bot",
                },
            ]);
            setInput("");
        } catch (e) {
            console.log(e);
        }
    };

    return (
        <div className="flex flex-col h-full">
            <div
                ref={scrollRef}
                className="flex-1 overflow-y-auto space-y-2 pr-2 pl-2 pt-4 scrollbar-hide bg-gray-800"
            >
                {messages.map((msg: Message, index) => (
                    <MessageBubble
                        key={index}
                        tagMessage={msg.tagMessage}
                        message={msg.message}
                        isSender={msg.isSender}
                    />
                ))}
            </div>

            <div className="mt-4 flex-shrink-0 flex pb-1 pl-1 pr-1">
                <input
                    className="flex-1 p-2 border rounded-l-xl outline-none"
                    placeholder="Message"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && sendMessage()}
                />
                <button
                    className="bg-gold text-dark px-1 rounded-r-xl"
                    onClick={sendMessage}
                >
                    Enviar
                </button>
            </div>
        </div>
    );
}
