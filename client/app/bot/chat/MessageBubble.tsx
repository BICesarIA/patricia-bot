type Message = {
    tagMessage: 'bot' | 'gpt' | 'seller' | 'client';
    message: string;
    isSender: boolean;
};

export default function MessageBubble({ tagMessage, message, isSender } : Message) {
    const tagStyles = {
        bot: {
            label: 'Bot (no GPT)',
            color: 'bg-green-100 text-green-800',
        },
        gpt: {
            label: 'Bot (GPT)',
            color: 'bg-yellow-100 text-yellow-800',
        },
        seller: {
            label: 'Vendedor',
            color: 'bg-purple-100 text-purple-800',
        },
        client: {
            label: 'Cliente',
            color: 'bg-purple-100 text-purple-800',
        },
    };

    const tag = tagStyles[tagMessage];

    return (
        <div className={`flex flex-col ${isSender ? 'items-end' : 'items-start'} mb-3`}>
            {tag && (
                <div
                    className={`text-xs px-2 py-0.5 rounded-full font-medium mb-1 ${tag.color}`}
                >
                    {tag.label}
                </div>
            )}
            <div
                className={`p-2 rounded-xl max-w-xs whitespace-pre-line ${isSender ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-800'
                    }`}
            >
                {message}
            </div>
        </div>
    );
}
