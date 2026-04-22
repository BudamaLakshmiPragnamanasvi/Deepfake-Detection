import { ShieldAlert, ShieldCheck } from 'lucide-react';
import { motion } from 'framer-motion';
import ConfidenceBar from './ConfidenceBar';

export default function ResultDisplay({ result }) {
  if (!result) return null;

  const isFake = result.label === "Fake";
  const Icon = isFake ? ShieldAlert : ShieldCheck;
  const bgColor = isFake ? 'bg-red-500/10' : 'bg-green-500/10';
  const textColor = isFake ? 'text-red-500' : 'text-green-500';
  const borderColor = isFake ? 'border-red-500/20' : 'border-green-500/20';

  return (
    <motion.div 
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className={`rounded-2xl p-6 border ${borderColor} ${bgColor} flex flex-col items-center justify-center text-center`}
    >
      <div className={`p-4 rounded-full mb-4 ${isFake ? 'bg-red-500/20' : 'bg-green-500/20'}`}>
        <Icon className={`w-12 h-12 ${textColor}`} />
      </div>
      
      <h2 className="text-3xl font-bold text-white mb-2 uppercase tracking-wider">
        {result.label}
      </h2>
      
      <p className="text-sm text-gray-300 mb-4 max-w-sm">
        {isFake 
          ? "The model detected manipulation artifacts consistent with a deepfake." 
          : "The image appears to be authentic with no visible manipulation artifacts."}
      </p>

      <ConfidenceBar label={result.label} confidence={result.confidence} />
    </motion.div>
  );
}
