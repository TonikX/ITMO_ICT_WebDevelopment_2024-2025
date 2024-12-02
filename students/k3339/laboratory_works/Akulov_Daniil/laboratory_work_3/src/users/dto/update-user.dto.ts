import {ApiProperty, OmitType, PartialType} from "@nestjs/swagger";
import {IsOptional, IsString, Length} from "class-validator";
import {CreateUserDto} from "./create-user.dto";

export class UpdateUserDto extends PartialType(OmitType(CreateUserDto, ['password'] as const)) {
    @ApiProperty({example: 'Profile desc :)'})
    @IsOptional()
    @IsString({message: 'Description must be string'})
    @Length(0, 140, {message: 'Description length must be less then 140'})
    readonly description?: string;
}