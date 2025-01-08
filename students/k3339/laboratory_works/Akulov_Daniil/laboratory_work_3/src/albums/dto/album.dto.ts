import {ApiProperty} from "@nestjs/swagger";
import {IsBoolean, IsOptional, IsString, Length} from "class-validator";

export class AlbumDto {
    @ApiProperty({example: 'Heavy Metal 2'})
    @IsString({message: 'Album title must be string'})
    @Length(1, 40, {message: 'Album title length must be between 1 and 40'})
    readonly name: string;

    @ApiProperty({example: false})
    @IsOptional()
    @IsBoolean({message: 'Album private setting must be boolean'})
    readonly isPrivate: boolean;
}
