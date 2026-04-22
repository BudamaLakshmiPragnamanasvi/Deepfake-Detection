import { useState } from 'react';
import { Layers } from 'lucide-react';
import { motion } from 'framer-motion';

export default function GradCamViewer({ originalFile, gradCamBase64 }) {
  const [showOverlay, setShowOverlay] = useState(true);

  if (!gradCamBase64 || !originalFile) return null;

  const origUrl = URL.createObjectURL(originalFile);
  const gradCamUrl = `data:image/png;base64,${gradCamBase64}`;

  return (
    <div className="bg-gray-800/50 rounded-2xl p-6 border border-gray-700">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-white flex items-center gap-2">
          <Layers className="w-5 h-5 text-accent" />
          Explainability (Grad-CAM)
        </h3>
        <button
          onClick={() => setShowOverlay(!showOverlay)}
          className="text-xs font-medium px-3 py-1.5 rounded-md bg-gray-700 hover:bg-gray-600 transition-colors text-white"
        >
          {showOverlay ? 'Show Original' : 'Show Heatmap'}
        </button>
      </div>

      <div className="relative rounded-xl overflow-hidden bg-black aspect-square max-w-sm mx-auto border border-gray-700">
        {/* Original */}
        <img 
          src={origUrl} 
          alt="Original" 
          className="absolute inset-0 w-full h-full object-contain"
        />
        
        {/* Heatmap Overlay */}
        <motion.img 
          initial={false}
          animate={{ opacity: showOverlay ? 1 : 0 }}
          transition={{ duration: 0.3 }}
          src={gradCamUrl} 
          alt="Grad-CAM Heatmap" 
          className="absolute inset-0 w-full h-full object-contain mix-blend-screen"
        />
      </div>
      <p className="text-xs text-gray-400 text-center mt-3">
        Heatmap highlights regions the model focused on to make its decision.
      </p>
    </div>
  );
}
