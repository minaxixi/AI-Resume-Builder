import React, { useRef } from 'react';
import { Button, FormControl, FormLabel, Input, HStack } from '@chakra-ui/react';

interface FileUploadProps {
  onFileSelect: (file: File) => void;
  selectedFile: File | null;
}

export const FileUpload: React.FC<FileUploadProps> = ({ onFileSelect, selectedFile }) => {
  const inputRef = useRef<HTMLInputElement>(null);

  const handleClick = () => {
    inputRef.current?.click();
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      onFileSelect(file);
    }
  };

  return (
    <FormControl isRequired>
      <FormLabel>Resume (PDF)</FormLabel>
      <HStack>
        <Input
          type="file"
          accept=".pdf"
          onChange={handleFileChange}
          display="none"
          ref={inputRef}
        />
        <Button onClick={handleClick} size="md" width="200px">
          Choose PDF File
        </Button>
        {selectedFile && (
          <Input
            value={selectedFile.name}
            isReadOnly
            placeholder="No file selected"
            size="md"
            flex="1"
          />
        )}
      </HStack>
    </FormControl>
  );
};
