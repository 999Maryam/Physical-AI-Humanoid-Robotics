import React, { useState, useEffect } from 'react';
import Content from '@theme-original/DocItem/Content';
import { useLocation } from '@docusaurus/router';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import LanguageSwitcher from '../../../components/LanguageSwitcher';
import { getPersonalizedChapterContent } from '../../../services/personalization_api';

const fetchTranslatedContent = async (chapterId, targetLanguage) => {
  try {
    const response = await fetch(`/api/v1/chapters/${chapterId}/translate?target_language=${targetLanguage}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data.translated_text;
  } catch (error) {
    console.error('Error fetching translated content:', error);
    return null;
  }
};

const isPersonalizationEnabled = true; // This would come from a feature flag or user setting
const mockUserId = "user123"; // Mock user ID for demonstration

export default function ContentWrapper(props) {
  const { pathname } = useLocation();
  const { i18n } = useDocusaurusContext();
  const { currentLocale } = i18n;
  const [translatedContent, setTranslatedContent] = useState(null);
  const [personalizedContent, setPersonalizedContent] = useState(null);
  const [chapterId, setChapterId] = useState(null);

  useEffect(() => {
    // Extract chapter ID from pathname, e.g., /docs/intro-to-physical-ai becomes intro-to-physical-ai
    const pathParts = pathname.split('/').filter(Boolean);
    const currentChapterId = pathParts[pathParts.length - 1];
    setChapterId(currentChapterId);

    if (currentLocale === 'ur' && currentChapterId) {
      fetchTranslatedContent(currentChapterId, 'ur').then(content => {
        setTranslatedContent(content);
        // If personalization is also enabled, fetch personalized version of translated content
        if (isPersonalizationEnabled && mockUserId && content) {
          getPersonalizedChapterContent(mockUserId, currentChapterId, content).then(pContent => {
            setPersonalizedContent(pContent);
          });
        } else {
          setPersonalizedContent(null);
        }
      });
    } else if (isPersonalizationEnabled && mockUserId && currentChapterId) {
        // If no translation, but personalization is enabled, fetch personalized original content
        // You would need to fetch the original content first before personalizing
        // For simplicity, let's assume props.children.props.children is the original content for now (adjust as needed)
        const originalContent = props.children.props.children; // Docusaurus specific way to get content
        if (originalContent) {
          getPersonalizedChapterContent(mockUserId, currentChapterId, originalContent).then(pContent => {
            setPersonalizedContent(pContent);
          });
        }
        setTranslatedContent(null);
    } else {
      setTranslatedContent(null);
      setPersonalizedContent(null);
    }
  }, [pathname, currentLocale, props.children.props.children]); // Added props.children.props.children to dependencies
  return (
    <>
      <LanguageSwitcher currentPath={pathname} />
      {isPersonalizationEnabled && personalizedContent ? (
        <div dangerouslySetInnerHTML={{ __html: personalizedContent }} />
      ) : currentLocale === 'ur' && translatedContent ? (
        <div dangerouslySetInnerHTML={{ __html: translatedContent }} />
      ) : (
        <Content {...props} />
      )}
    </>
  );
}
