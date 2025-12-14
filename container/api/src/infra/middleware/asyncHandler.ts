import { Request, Response, NextFunction, RequestHandler } from 'express';

/**
 * Async error handler wrapper for Express routes
 * Catches async errors and passes them to Express error middleware
 */
export const asyncHandler = (fn: RequestHandler): RequestHandler => {
  return (req: Request, res: Response, next: NextFunction) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };
};
