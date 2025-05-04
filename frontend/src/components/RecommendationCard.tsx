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
import { GiftIdea } from '../services/api';

interface RecommendationCardProps {
  recommendation: GiftIdea;
}

const RecommendationCard = ({ recommendation }: RecommendationCardProps) => {
  const { name, description, link } = recommendation;
  
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
        </HStack>
        
        <Text>{description}</Text>
        
        {link && (
          <Link href={link} isExternal color="blue.500" fontWeight="medium">
            View Product →
          </Link>
        )}
      </VStack>
    </Box>
  );
};

export default RecommendationCard; 