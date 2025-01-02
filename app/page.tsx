'use client'

import { useState } from 'react'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

export default function FeedbackForm() {
  const [feedbackText, setFeedbackText] = useState('')
  const [feedbackType, setFeedbackType] = useState('')
  const [suggestion, setSuggestion] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    try {
      const response = await fetch('http://localhost:3000/api/feedback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ feedbackText, feedbackType }),
      })
      const data = await response.json()
      setSuggestion(data.suggestion)
    } catch (error) {
      console.error('Error submitting feedback:', error)
      setSuggestion('Failed to fetch suggestion. Please try again.')
    }
    setIsLoading(false)
  }

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>Feedback Form</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="feedbackText">Your Feedback</Label>
              <Input
                id="feedbackText"
                placeholder="Enter your feedback here"
                value={feedbackText}
                onChange={(e) => setFeedbackText(e.target.value)}
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="feedbackType">Feedback Type</Label>
              <Select value={feedbackType} onValueChange={setFeedbackType} required>
                <SelectTrigger id="feedbackType">
                  <SelectValue placeholder="Select feedback type" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="Bug">Bug</SelectItem>
                  <SelectItem value="Idea">Idea</SelectItem>
                  <SelectItem value="Other">Other</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <Button type="submit" className="w-full" disabled={isLoading}>
              {isLoading ? 'Submitting...' : 'Submit Feedback'}
            </Button>
          </form>
          {suggestion && (
            <div className="mt-4 p-4 bg-gray-50 rounded-md">
              <h3 className="font-semibold mb-2">AI Suggestion:</h3>
              <p>{suggestion}</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}

