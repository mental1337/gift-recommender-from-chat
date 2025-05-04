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
  Spinner,
  Alert,
  AlertIcon,
  SimpleGrid,
  useToast,
  FormControl,
  FormLabel,
  HStack,
} from '@chakra-ui/react';
import { FiUpload } from 'react-icons/fi';
import apiService, { GiftIdea, GiftRecommendations } from '../services/api';
import RecommendationCard from './RecommendationCard';

const HomePage = () => {
  const [file, setFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [recommendations, setRecommendations] = useState<GiftIdea[]>([]);
  const [notes, setNotes] = useState<string>('');
  const [userName, setUserName] = useState('');
  const [friendName, setFriendName] = useState('');
  const fileInputRef = useRef<HTMLInputElement>(null);
  const toast = useToast();

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
      // Reset any previous results
      setRecommendations([]);
      setNotes('');
      setError(null);
      console.log('File uploaded:', droppedFile.name);
    }
  }, []);

  const handleFileChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const selectedFile = e.target.files[0];
      setFile(selectedFile);
      // Reset any previous results
      setRecommendations([]);
      setNotes('');
      setError(null);
      console.log('File selected:', selectedFile.name);
    }
  }, []);

  const handleClick = useCallback(() => {
    fileInputRef.current?.click();
  }, []);

  const handleAnalyze = async () => {
    if (!file) return;
    
    if (!userName.trim()) {
      toast({
        title: 'Missing information',
        description: 'Please enter your name.',
        status: 'warning',
        duration: 3000,
        isClosable: true,
      });
      return;
    }
    
    if (!friendName.trim()) {
      toast({
        title: 'Missing information',
        description: 'Please enter your friend\'s name.',
        status: 'warning',
        duration: 3000,
        isClosable: true,
      });
      return;
    }
    
    setIsLoading(true);
    setError(null);
    setRecommendations([]);
    setNotes('');
    
    try {
      const result = await apiService.uploadChatHistory(file, userName, friendName);
      setRecommendations(result.gift_ideas);
      setNotes(result.notes);
      
      if (result.gift_ideas.length === 0) {
        toast({
          title: 'No recommendations found',
          description: 'We couldn\'t generate any recommendations from this chat history. Try uploading a different file.',
          status: 'info',
          duration: 5000,
          isClosable: true,
        });
      }
    } catch (err) {
      console.error('Error analyzing chat:', err);
      setError('Failed to analyze chat history. Please try again later.');
      toast({
        title: 'Error',
        description: 'Failed to analyze chat history. Please try again later.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  const bgColor = useColorModeValue('gray.50', 'gray.700');
  const borderColor = useColorModeValue('gray.200', 'gray.600');
  const activeBorderColor = useColorModeValue('blue.400', 'blue.300');
  const notesBgColor = useColorModeValue('blue.50', 'blue.900');
  const notesBorderColor = useColorModeValue('blue.200', 'blue.700');

  return (
    <Container maxW="container.xl" py={10}>
      <VStack spacing={8} align="stretch">
        <Heading as="h1" size="xl" textAlign="center">
          Gift Recommender From Chat
        </Heading>
        
        <Box p={6} borderRadius="lg" bg={bgColor}>
          <VStack spacing={5}>
            <Heading as="h2" size="md">
              Upload Chat History
            </Heading>
            <Text textAlign="center">
              Upload your chat history file to get personalized gift recommendations for your friend.
            </Text>
            
            <HStack width="100%" spacing={4} wrap={{ base: "wrap", md: "nowrap" }}>
              <FormControl isRequired>
                <FormLabel>Your Name</FormLabel>
                <Input 
                  placeholder="Enter your name" 
                  value={userName} 
                  onChange={(e) => setUserName(e.target.value)}
                />
              </FormControl>
              
              <FormControl isRequired>
                <FormLabel>Friend's Name</FormLabel>
                <Input 
                  placeholder="Enter your friend's name" 
                  value={friendName} 
                  onChange={(e) => setFriendName(e.target.value)}
                />
              </FormControl>
            </HStack>
            
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
              <Button 
                colorScheme="blue" 
                width="full" 
                onClick={handleAnalyze} 
                isLoading={isLoading}
                loadingText="Analyzing Chat"
              >
                Analyze Chat & Get Recommendations
              </Button>
            )}
          </VStack>
        </Box>
        
        {isLoading && (
          <Flex justify="center" pt={10}>
            <VStack>
              <Spinner size="xl" color="blue.500" thickness="4px" />
              <Text fontWeight="medium" mt={4}>
                Analyzing chat and generating recommendations...
              </Text>
            </VStack>
          </Flex>
        )}
        
        {error && (
          <Alert status="error" borderRadius="md">
            <AlertIcon />
            {error}
          </Alert>
        )}
        
        {recommendations.length > 0 && (
          <Box mt={6}>
            <Heading as="h2" size="lg" mb={4}>
              Gift Recommendations for {friendName}
            </Heading>
            
            {notes && (
              <Box 
                p={4} 
                mb={6} 
                bg={notesBgColor} 
                borderRadius="md" 
                borderWidth="1px" 
                borderColor={notesBorderColor}
              >
                <Heading as="h3" size="sm" mb={2}>
                  Analysis Notes
                </Heading>
                <Text whiteSpace="pre-wrap">{notes}</Text>
              </Box>
            )}
            
            <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6}>
              {recommendations.map((recommendation, index) => (
                <RecommendationCard key={index} recommendation={recommendation} />
              ))}
            </SimpleGrid>
          </Box>
        )}
      </VStack>
    </Container>
  );
};

export default HomePage; 