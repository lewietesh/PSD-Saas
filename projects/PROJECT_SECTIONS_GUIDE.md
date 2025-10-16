# Project Sections Implementation Guide

## Overview

The project sections feature allows you to create detailed, multi-section project showcases with images and descriptions. This guide explains why we chose the current implementation and how to use it.

## Architecture Decision: URLs vs File Uploads

### Why We Use URLs (Not File Uploads) for Sections

**Decision**: Store media URLs in JSONField instead of creating file upload fields

**Reasons**:

1. **Database Efficiency**
   - No additional tables or joins required
   - Single query retrieves all project data including sections
   - Better API performance

2. **Flexibility**
   - Can reference internal uploads OR external URLs
   - Easy to reorganize sections without file management issues
   - Simple JSON structure for frontend consumption

3. **Simplicity**
   - No orphaned file cleanup needed when sections are edited/removed
   - Straightforward serialization for API responses
   - Easy to validate and preview

4. **Avoiding Complexity**
   - File uploads in JSONField would require storing paths (strings anyway)
   - Would need separate ProjectSectionMedia model (adds complexity)
   - File management becomes complex with JSON edits

## How to Use Project Sections in Admin

### Step-by-Step Process

1. **Upload Section Images**
   - Scroll to "Gallery Images" inline section
   - Click "Add another Project Gallery Image"
   - Upload your image (JPG, JPEG, PNG, WEBP - max 12MB)
   - Add alt text for accessibility
   - Set sort order
   - Save the project

2. **Copy Image URL**
   - After saving, the uploaded image URL will be visible
   - Format: `/media/projects/gallery/your-image.jpg`
   - Copy this URL

3. **Add to Sections Field**
   - Go to "Project Sections" fieldset
   - Use the JSON format:
   ```json
   [
     {
       "section_id": "overview",
       "media_url": "/media/projects/gallery/your-image.jpg",
       "description": "Detailed description of this section"
     }
   ]
   ```

4. **Add Multiple Sections**
   - Add more objects to the array for multiple sections
   - Each section needs: section_id, media_url, description

### Common Section IDs

- `overview` - Project introduction and overview
- `features` - Key features and functionality
- `architecture` - Technical architecture
- `tech-stack` - Technologies used
- `challenge` - Problems solved
- `solution` - How you solved them
- `results` - Outcomes and metrics
- `testimonial` - Client feedback
- `design` - Design process
- `development` - Development approach

## JSON Format Specification

```json
[
  {
    "section_id": "string (required) - identifier for this section",
    "media_url": "string (required) - /media/ path or http(s):// URL",
    "description": "string (required) - detailed section content"
  }
]
```

### Validation Rules

✅ Must be a valid JSON array
✅ Each section must be an object with all 3 required fields
✅ media_url must start with `/media/`, `http://`, or `https://`
✅ section_id should be lowercase with hyphens (e.g., tech-stack)

## Alternative: External URLs

You can also use external image URLs:

```json
[
  {
    "section_id": "overview",
    "media_url": "https://example.com/project-screenshot.jpg",
    "description": "Project overview..."
  }
]
```

## Benefits of This Approach

1. ✅ **User-Friendly Admin**: Clear instructions and validation
2. ✅ **Efficient Queries**: No joins, single query performance
3. ✅ **Flexible**: Internal or external media
4. ✅ **Maintainable**: Simple to update and reorganize
5. ✅ **API-Ready**: Direct JSON serialization

## Future Enhancements (Optional)

If you need even more user-friendliness, consider:

- Custom admin page with drag-and-drop section builder
- Inline JavaScript to copy URLs from gallery images
- Visual section editor with live preview
- Separate ProjectSection model (trade-off: more complex queries)

---

**Note**: This implementation prioritizes performance and simplicity while maintaining good UX through clear documentation and validation.
