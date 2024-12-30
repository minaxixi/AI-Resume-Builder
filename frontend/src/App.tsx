import React, { useState } from 'react';
import {
  ChakraProvider,
  Container,
  VStack,
  Heading,
  FormControl,
  FormLabel,
  Input,
  Button,
  Text,
  Box,
  Progress,
  SimpleGrid,
  Card,
  CardHeader,
  CardBody,
  Switch,
  HStack,
  useToast,
} from '@chakra-ui/react';
import { uploadAndTailorResume, TailorResponse } from './services/api';
import DiffView from './components/DiffView';

interface AppProps {}

function App(props: AppProps) {
  const [file, setFile] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<TailorResponse | null>(null);
  const [showDiff, setShowDiff] = useState(false);
  const toast = useToast();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) {
      toast({
        title: 'Missing resume',
        description: 'Please upload your resume PDF file',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
      return;
    }
    
    if (!jobDescription.trim()) {
      toast({
        title: 'Missing job description',
        description: 'Please provide the job description URL',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
      return;
    }

    setIsLoading(true);
    try {
      const response = await uploadAndTailorResume(file, jobDescription);
      setResult(response);
      toast({
        title: 'Success',
        description: 'Resume has been tailored successfully',
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
    } catch (error: any) {
      console.error('Error:', error);
      toast({
        title: 'Error',
        description: error.message || 'Failed to process resume. Please try again.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
      setResult(null);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <ChakraProvider>
      <Container maxW="container.xl" py={10}>
        <VStack spacing={8} align="stretch">
          <Heading textAlign="center">AI Resume Tailor</Heading>
          
          <Box p={4} borderRadius="md" bg="blue.50">
            <Text>
              Upload your resume (PDF format) and provide the job description URL to get a tailored version of your resume.
            </Text>
          </Box>

          <form onSubmit={handleSubmit}>
            <HStack spacing={2} width="100%" alignItems="flex-end">
              <FormControl isRequired width="450px">
                <FormLabel>Resume (PDF)</FormLabel>
                <HStack spacing={2}>
                  <Button
                    onClick={() => document.getElementById('resume-upload')?.click()}
                    size="md"
                    width="150px"
                  >
                    Choose PDF File
                  </Button>
                  <Input
                    id="resume-upload"
                    type="file"
                    accept=".pdf"
                    onChange={(e) => {
                      const file = e.target.files?.[0];
                      if (file) setFile(file);
                    }}
                    display="none"
                  />
                  {file && (
                    <Input
                      value={file.name}
                      isReadOnly
                      placeholder="No file selected"
                      size="md"
                      width="280px"
                    />
                  )}
                </HStack>
              </FormControl>

              <FormControl isRequired flex="1">
                <FormLabel>Job Description URL</FormLabel>
                <Input
                  value={jobDescription}
                  onChange={(e) => setJobDescription(e.target.value)}
                  placeholder="Enter job description URL"
                  type="url"
                  size="md"
                />
              </FormControl>

              <Button
                type="submit"
                colorScheme="blue"
                isLoading={isLoading}
                loadingText="Processing..."
                width="150px"
                size="md"
                disabled={!file || !jobDescription.trim()}
              >
                Tailor Resume
              </Button>
            </HStack>
          </form>

          {isLoading && (
            <Box>
              <Progress size="xs" isIndeterminate />
              <Text mt={2} textAlign="center" color="gray.600">
                Tailoring your resume... This may take a few moments.
              </Text>
            </Box>
          )}

          {result && (
            <VStack spacing={4}>
              <HStack>
                <FormControl display="flex" alignItems="center">
                  <FormLabel htmlFor="diff-toggle" mb="0">
                    Highlight Changes
                  </FormLabel>
                  <Switch
                    id="diff-toggle"
                    isChecked={showDiff}
                    onChange={(e) => setShowDiff(e.target.checked)}
                  />
                </FormControl>
              </HStack>

              <SimpleGrid columns={2} spacing={4} width="100%">
                <Card>
                  <CardHeader>
                    <Heading size="md">Original Resume</Heading>
                  </CardHeader>
                  <CardBody>
                    <Box
                      whiteSpace="pre-wrap"
                      fontFamily="monospace"
                      p={4}
                      borderRadius="md"
                      bg="gray.50"
                      minHeight="500px"
                      maxHeight="800px"
                      overflowY="auto"
                    >
                      {result.original_text}
                    </Box>
                  </CardBody>
                </Card>

                <Card>
                  <CardHeader>
                    <Heading size="md">Tailored Resume</Heading>
                  </CardHeader>
                  <CardBody>
                    <DiffView
                      originalText={result.original_text}
                      newText={result.enhanced_text}
                      showDiff={showDiff}
                    />
                  </CardBody>
                </Card>
              </SimpleGrid>
            </VStack>
          )}
        </VStack>
      </Container>
    </ChakraProvider>
  );
}

export default App;
