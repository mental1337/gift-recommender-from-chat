import { useState, useRef, useCallback } from 'react';
import {
  Box,
  Button,
  Container,
  Flex,
  Heading,
  Text,
  VStack,
  useColorModeValue,
  Icon,
  Input,
} from '@chakra-ui/react';
import { FiUpload } from 'react-icons/fi';

const HomePage = () => {
  const [file, setFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const droppedFile = e.dataTransfer.files[0];
      setFile(droppedFile);
      // Handle file upload logic here
      console.log('File uploaded:', droppedFile.name);
    }
  }, []);

  const handleFileChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const selectedFile = e.target.files[0];
      setFile(selectedFile);
      // Handle file upload logic here
      console.log('File selected:', selectedFile.name);
    }
  }, []);

  const handleClick = useCallback(() => {
    fileInputRef.current?.click();
  }, []);

  const bgColor = useColorModeValue('gray.50', 'gray.700');
  const borderColor = useColorModeValue('gray.200', 'gray.600');
  const activeBorderColor = useColorModeValue('blue.400', 'blue.300');

  return (
    <Container maxW="container.xl" py={10}>
      <VStack spacing={8} align="stretch">
        <Heading as="h1" size="xl" textAlign="center">
          Gift Recommender From Chat
        </Heading>
        
        <Box p={6} borderRadius="lg" bg={bgColor}>
          <VStack spacing={4}>
            <Heading as="h2" size="md">
              Upload Chat History
            </Heading>
            <Text textAlign="center">
              Upload your chat history file to get personalized gift recommendations for your friend.
            </Text>
            
            <Flex 
              direction="column" 
              align="center" 
              justify="center"
              p={8}
              border="2px dashed"
              borderColor={isDragging ? activeBorderColor : borderColor}
              borderRadius="md"
              bg={isDragging ? 'gray.100' : 'transparent'}
              transition="all 0.2s"
              w="100%"
              h="200px"
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              onClick={handleClick}
              cursor="pointer"
            >
              <Input
                type="file"
                ref={fileInputRef}
                onChange={handleFileChange}
                display="none"
                accept=".txt,.json,.csv"
              />
              <Icon as={FiUpload} w={10} h={10} mb={4} color={isDragging ? activeBorderColor : 'gray.500'} />
              
              {file ? (
                <Text fontWeight="bold">
                  File selected: {file.name}
                </Text>
              ) : (
                <VStack spacing={2}>
                  <Text fontWeight="medium">
                    Drag and drop your file here
                  </Text>
                  <Text fontSize="sm" color="gray.500">
                    or click to browse
                  </Text>
                </VStack>
              )}
            </Flex>
            
            {file && (
              <Button colorScheme="blue" width="full">
                Analyze Chat & Get Recommendations
              </Button>
            )}
          </VStack>
        </Box>
      </VStack>
    </Container>
  );
};

export default HomePage; 