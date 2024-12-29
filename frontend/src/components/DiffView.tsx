import React from 'react';
import { Box } from '@chakra-ui/react';
import { diff_match_patch, Diff } from 'diff-match-patch';

interface DiffViewProps {
  originalText: string;
  newText: string;
  showDiff: boolean;
}

const DiffView: React.FC<DiffViewProps> = ({ originalText, newText, showDiff }) => {
  const computeDiff = () => {
    if (!showDiff) return newText;

    const dmp = new diff_match_patch();
    const diff = dmp.diff_main(originalText, newText);
    dmp.diff_cleanupSemantic(diff);

    return diff.map((diffItem: Diff, index: number) => {
      const [type, text] = diffItem;
      switch (type) {
        case 1: // Insertion
          return (
            <span key={index} style={{ backgroundColor: '#e6ffe6' }}>
              {text}
            </span>
          );
        case -1: // Deletion
          return (
            <span key={index} style={{ backgroundColor: '#ffe6e6', textDecoration: 'line-through' }}>
              {text}
            </span>
          );
        default: // No change
          return <span key={index}>{text}</span>;
      }
    });
  };

  return (
    <Box
      fontFamily="monospace"
      whiteSpace="pre-wrap"
      p={4}
      borderRadius="md"
      bg="gray.50"
      minHeight="500px"
      maxHeight="800px"
      overflowY="auto"
    >
      {computeDiff()}
    </Box>
  );
};

export default DiffView;
