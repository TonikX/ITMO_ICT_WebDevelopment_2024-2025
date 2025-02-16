namespace Server;

public class ProducerConsumerStream : Stream
{
    private readonly byte[] _currentBuffer = new byte[1024 * 32];

    public override bool CanRead => true;
    public override bool CanSeek => false;
    public override bool CanWrite => true;
    public override long Length => throw new NotSupportedException();

    public override long Position { get; set; }
    private int _writePosition;

    public override void Flush()
    {
    }

    public override int Read(byte[] buffer, int offset, int count)
    {
        while (_writePosition - (int)Position == 0) 
            Thread.Sleep(10);
        
        var bytesToCopy = Math.Min(count, _writePosition - (int)Position);
        if (bytesToCopy == 0)
            return 0;

        Array.Copy(_currentBuffer, Position, buffer, offset, bytesToCopy);
        Position += bytesToCopy;
        return bytesToCopy;
    }

    public override void Write(byte[] buffer, int offset, int count)
    {
        if (_writePosition + count > _currentBuffer.Length)
            throw new InvalidOperationException("Buffer is full");

        Array.Copy(buffer, offset, _currentBuffer, _writePosition, count);
        _writePosition += count;
    }

    public override long Seek(long offset, SeekOrigin origin)
    {
        throw new NotSupportedException();
    }

    public override void SetLength(long value)
    {
        throw new NotSupportedException();
    }
}