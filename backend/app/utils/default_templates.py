"""
Default chapter template library
Contains pre-built templates for common chapter types
"""

DEFAULT_TEMPLATES = [
    {
        "name": "Simple Text Chapter",
        "description": "A basic text-only chapter with no special formatting or interactivity.",
        "is_public": True,
        "template_data": {
            "type": "simple",
            "structure": {
                "text": "Your chapter text goes here..."
            }
        }
    },
    {
        "name": "Visual Novel - Dialogue Scene",
        "description": "A visual novel style template with character sprites, dialogue boxes, and background images.",
        "is_public": True,
        "template_data": {
            "type": "interactive",
            "nodes": [
                {
                    "id": "start",
                    "type": "scene",
                    "background": "placeholder_background.jpg",
                    "music": None,
                    "next": "dialogue1"
                },
                {
                    "id": "dialogue1",
                    "type": "dialogue",
                    "character": "Character Name",
                    "sprite": "character_sprite.png",
                    "text": "This is a sample dialogue line.",
                    "next": "dialogue2"
                },
                {
                    "id": "dialogue2",
                    "type": "dialogue",
                    "character": "Another Character",
                    "sprite": "another_character.png",
                    "text": "This is another character's response.",
                    "next": "end"
                }
            ]
        }
    },
    {
        "name": "Choice-Based Chapter",
        "description": "A chapter with branching storyline based on reader choices.",
        "is_public": True,
        "template_data": {
            "type": "interactive",
            "nodes": [
                {
                    "id": "start",
                    "type": "text",
                    "content": "You find yourself at a crossroads. Which path do you take?",
                    "next": "choice1"
                },
                {
                    "id": "choice1",
                    "type": "choice",
                    "question": "Choose your path:",
                    "options": [
                        {
                            "text": "Take the left path through the forest",
                            "next": "left_path"
                        },
                        {
                            "text": "Take the right path along the river",
                            "next": "right_path"
                        }
                    ]
                },
                {
                    "id": "left_path",
                    "type": "text",
                    "content": "You venture into the dark forest...",
                    "next": "end"
                },
                {
                    "id": "right_path",
                    "type": "text",
                    "content": "You follow the river downstream...",
                    "next": "end"
                }
            ]
        }
    },
    {
        "name": "Animated Text Chapter",
        "description": "A chapter with text animations and visual effects.",
        "is_public": True,
        "template_data": {
            "type": "interactive",
            "nodes": [
                {
                    "id": "start",
                    "type": "text",
                    "content": "Chapter text with fade-in animation",
                    "animation": "fadeIn",
                    "duration": 1000,
                    "next": "text2"
                },
                {
                    "id": "text2",
                    "type": "text",
                    "content": "This text slides in from the left",
                    "animation": "slideInLeft",
                    "duration": 800,
                    "next": "text3"
                },
                {
                    "id": "text3",
                    "type": "text",
                    "content": "This text appears with a typing effect",
                    "animation": "typewriter",
                    "duration": 2000,
                    "next": "end"
                }
            ]
        }
    },
    {
        "name": "Image Gallery Chapter",
        "description": "A chapter featuring multiple images with captions.",
        "is_public": True,
        "template_data": {
            "type": "interactive",
            "nodes": [
                {
                    "id": "start",
                    "type": "text",
                    "content": "Introduction text for your image gallery...",
                    "next": "image1"
                },
                {
                    "id": "image1",
                    "type": "image",
                    "src": "image1.jpg",
                    "alt": "Image description",
                    "caption": "Caption for the first image",
                    "next": "image2"
                },
                {
                    "id": "image2",
                    "type": "image",
                    "src": "image2.jpg",
                    "alt": "Image description",
                    "caption": "Caption for the second image",
                    "next": "conclusion"
                },
                {
                    "id": "conclusion",
                    "type": "text",
                    "content": "Concluding text after the images...",
                    "next": "end"
                }
            ]
        }
    },
    {
        "name": "Flashback Scene",
        "description": "A template for flashback scenes with visual indicators and transitions.",
        "is_public": True,
        "template_data": {
            "type": "interactive",
            "nodes": [
                {
                    "id": "start",
                    "type": "text",
                    "content": "Present day narrative...",
                    "next": "flashback_transition"
                },
                {
                    "id": "flashback_transition",
                    "type": "transition",
                    "effect": "blur_fade",
                    "text": "Ten years earlier...",
                    "style": {
                        "filter": "sepia(80%)",
                        "opacity": 0.9
                    },
                    "next": "flashback_content"
                },
                {
                    "id": "flashback_content",
                    "type": "text",
                    "content": "Flashback narrative content...",
                    "style": {
                        "filter": "sepia(80%)"
                    },
                    "next": "return_transition"
                },
                {
                    "id": "return_transition",
                    "type": "transition",
                    "effect": "fade",
                    "text": "Present day...",
                    "next": "present"
                },
                {
                    "id": "present",
                    "type": "text",
                    "content": "Back to present day narrative...",
                    "next": "end"
                }
            ]
        }
    },
    {
        "name": "Character Introduction",
        "description": "A template for introducing new characters with descriptions and images.",
        "is_public": True,
        "template_data": {
            "type": "interactive",
            "nodes": [
                {
                    "id": "start",
                    "type": "character_card",
                    "name": "Character Name",
                    "title": "Character Title/Role",
                    "image": "character_portrait.jpg",
                    "description": "Character description and background...",
                    "traits": [
                        "Trait 1",
                        "Trait 2",
                        "Trait 3"
                    ],
                    "next": "narrative"
                },
                {
                    "id": "narrative",
                    "type": "text",
                    "content": "Continue with the story...",
                    "next": "end"
                }
            ]
        }
    },
    {
        "name": "Combat/Action Scene",
        "description": "A template for action-packed combat scenes with dynamic effects.",
        "is_public": True,
        "template_data": {
            "type": "interactive",
            "nodes": [
                {
                    "id": "start",
                    "type": "text",
                    "content": "The battle begins!",
                    "style": {
                        "fontWeight": "bold",
                        "fontSize": "1.2em"
                    },
                    "next": "action1"
                },
                {
                    "id": "action1",
                    "type": "text",
                    "content": "You swing your sword!",
                    "animation": "shake",
                    "duration": 500,
                    "next": "choice1"
                },
                {
                    "id": "choice1",
                    "type": "choice",
                    "question": "What do you do next?",
                    "options": [
                        {
                            "text": "Attack again",
                            "next": "attack"
                        },
                        {
                            "text": "Defend",
                            "next": "defend"
                        },
                        {
                            "text": "Use special ability",
                            "next": "special"
                        }
                    ]
                },
                {
                    "id": "attack",
                    "type": "text",
                    "content": "You press the attack!",
                    "next": "end"
                },
                {
                    "id": "defend",
                    "type": "text",
                    "content": "You raise your shield defensively.",
                    "next": "end"
                },
                {
                    "id": "special",
                    "type": "text",
                    "content": "You unleash your ultimate technique!",
                    "animation": "pulse",
                    "next": "end"
                }
            ]
        }
    },
    {
        "name": "Mystery/Investigation",
        "description": "A template for mystery chapters with clue discovery and deduction.",
        "is_public": True,
        "template_data": {
            "type": "interactive",
            "nodes": [
                {
                    "id": "start",
                    "type": "text",
                    "content": "You examine the crime scene carefully...",
                    "next": "clue_search"
                },
                {
                    "id": "clue_search",
                    "type": "choice",
                    "question": "Where do you investigate first?",
                    "options": [
                        {
                            "text": "Examine the desk",
                            "next": "desk_clue"
                        },
                        {
                            "text": "Check the window",
                            "next": "window_clue"
                        },
                        {
                            "text": "Inspect the floor",
                            "next": "floor_clue"
                        }
                    ]
                },
                {
                    "id": "desk_clue",
                    "type": "clue",
                    "title": "Mysterious Letter",
                    "content": "You find a letter with strange symbols...",
                    "image": "letter.jpg",
                    "next": "deduction"
                },
                {
                    "id": "window_clue",
                    "type": "clue",
                    "title": "Broken Window Latch",
                    "content": "The window latch appears to have been forced open...",
                    "next": "deduction"
                },
                {
                    "id": "floor_clue",
                    "type": "clue",
                    "title": "Muddy Footprints",
                    "content": "You notice fresh muddy footprints leading away...",
                    "next": "deduction"
                },
                {
                    "id": "deduction",
                    "type": "text",
                    "content": "You piece together the clues...",
                    "next": "end"
                }
            ]
        }
    },
    {
        "name": "Emotional Scene",
        "description": "A template for emotionally charged scenes with atmosphere and pacing.",
        "is_public": True,
        "template_data": {
            "type": "interactive",
            "nodes": [
                {
                    "id": "start",
                    "type": "scene",
                    "background": "emotional_background.jpg",
                    "music": "sad_theme.mp3",
                    "ambience": "rain",
                    "next": "text1"
                },
                {
                    "id": "text1",
                    "type": "text",
                    "content": "The rain fell softly as they said their goodbyes...",
                    "animation": "fadeIn",
                    "duration": 2000,
                    "style": {
                        "fontStyle": "italic"
                    },
                    "next": "dialogue1"
                },
                {
                    "id": "dialogue1",
                    "type": "dialogue",
                    "character": "Character A",
                    "text": "I'll never forget you...",
                    "emotion": "sad",
                    "next": "dialogue2"
                },
                {
                    "id": "dialogue2",
                    "type": "dialogue",
                    "character": "Character B",
                    "text": "This isn't goodbye. It's see you later.",
                    "emotion": "hopeful",
                    "next": "conclusion"
                },
                {
                    "id": "conclusion",
                    "type": "text",
                    "content": "They parted ways, knowing they would meet again someday...",
                    "animation": "fadeOut",
                    "next": "end"
                }
            ]
        }
    }
]


def get_default_templates():
    """Return the list of default templates"""
    return DEFAULT_TEMPLATES


def get_template_by_name(name: str):
    """Get a specific default template by name"""
    for template in DEFAULT_TEMPLATES:
        if template["name"] == name:
            return template
    return None

