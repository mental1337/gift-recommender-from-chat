import {
  Box,
  Heading,
  Text,
  Badge,
  Link,
  VStack,
  HStack,
  useColorModeValue,
} from '@chakra-ui/react';
import { GiftRecommendation } from '../services/api';

interface RecommendationCardProps {
  recommendation: GiftRecommendation;
}

const RecommendationCard = ({ recommendation }: RecommendationCardProps) => {
  const { name, description, confidence, url } = recommendation;
  
  // Format confidence as percentage
  const confidencePercent = Math.round(confidence * 100);
  
  // Determine confidence color based on percentage
  let confidenceColor = 'green';
  if (confidencePercent < 50) {
    confidenceColor = 'red';
  } else if (confidencePercent < 75) {
    confidenceColor = 'yellow';
  }
  
  const bgColor = useColorModeValue('white', 'gray.700');
  const borderColor = useColorModeValue('gray.200', 'gray.600');
  
  return (
    <Box 
      p={5} 
      shadow="md" 
      borderWidth="1px" 
      borderRadius="lg" 
      bg={bgColor}
      borderColor={borderColor}
      width="100%"
    >
      <VStack align="start" spacing={2}>
        <HStack justify="space-between" width="100%">
          <Heading fontSize="xl">{name}</Heading>
          <Badge colorScheme={confidenceColor} px={2} py={1} borderRadius="md">
            {confidencePercent}% Match
          </Badge>
        </HStack>
        
        <Text>{description}</Text>
        
        {url && (
          <Link href={url} isExternal color="blue.500" fontWeight="medium">
            View Product →
          </Link>
        )}
      </VStack>
    </Box>
  );
};

export default RecommendationCard; 